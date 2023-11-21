# NOTE: https://www.pysimplegui.org/en/latest/cookbook/#recipe-long-operations-multi-threading iw a helpful link for threading

# NOTE: import libraries
import PySimpleGUI as sg
import threading
from speech import speech_recognition, open_pin, close_pin
import constant

# NOTE: This is for test
import cv2
import time

# NOTE: import other py files
import webcam

# TODO:
# Read a keyword from the repo every week

# NOTE:
# Initialization below

# NOTE:
# Global variables
calling_speech = False

# TODO:
# Layout GUI (I might need another file)

CIRCLE = '⚫'
CIRCLE_OUTLINE = '⚪'

def LED(color, key, mark=CIRCLE_OUTLINE):
    """
    A "user defined element".  In this case our LED is based on a Text element. This gives up 1 location to change how they look, size, etc.
    :param color: (str) The color of the LED
    :param key: (Any) The key used to look up the element
    :return: (sg.Text) Returns a Text element that displays the circle
    """
    return sg.Text(mark, text_color=color, key=key)

initial_page = [
    [sg.Text("Start Application")],
    [sg.Button("Start", size=(20, 2))]
]

image_viewer = [
    [sg.Text("Image From the Camera")],
    [sg.Image(key="-IMAGE-")],
]

stage_indicator = [
    [sg.Text("Default"), LED("Red", "-LED1-", CIRCLE)],
    [sg.Text("Face Detected"), LED("Red", "-LED2-")],
    [sg.Text("Password Passed"), LED("Red", "-LED3-")],
    [sg.Text("Password Failed - Try Again"), LED("Red", "-LED4-")],
    [sg.Text("Password Failed - Good Bye"), LED("Red", "-LED5-")]
]

processing_page = [
    [
        sg.Column(image_viewer),
        sg.VSeperator(),
        sg.Column(stage_indicator)
    ]
]

layout = [
    [
        sg.Column(initial_page, key='-COLINIT-', element_justification='c'),
        sg.Column(processing_page, key='-COLPROCESS-', visible=False)
    ],
    [sg.Button("Exit", size=(10, 1)), sg.Push(), sg.Button("Stop", visible=False, size=(10, 1))]
]

window = sg.Window("Open Sesame Application", layout, size=(1100, 700), element_justification='c')

def switchUIinStarting(turnOn: bool):
    window["-COLINIT-"].update(visible=not turnOn)
    window["-COLPROCESS-"].update(visible=turnOn)
    window["Stop"].update(visible=turnOn)

def changeState(fromState: int, toState: int):
    window[f'-LED{fromState}-'].update(CIRCLE_OUTLINE)
    window[f'-LED{toState}-'].update(CIRCLE)

def functionInThread(window: sg.Window):
    right_word = speech_recognition()
    window.write_event_value('-SPEECH DONE-', right_word)
    time.sleep(2)
    window.write_event_value('-CLOSE PIN-', right_word)

def createThread():
    threading.Thread(target=functionInThread, args=(window, ), daemon=True).start()

def closeAllPins():
    for i in range(2, 9):
        close_pin(i)

webCam = webcam.WebCamera()
closeAllPins()


while True:
    event, values = window.read(timeout=20)

    if event == "Exit" or event == sg.WIN_CLOSED:
        closeAllPins()
        break

    if event == "Start":
        switchUIinStarting(True)
        open_pin(2)
    elif event == "Stop":
        switchUIinStarting(False)
        closeAllPins()
    elif event == "-SPEECH DONE-":
        calling_speech = False
        close_pin(3)
        if values["-SPEECH DONE-"]:
            open_pin(4)
            changeState(2, 3)
        else:
            open_pin(5)
            changeState(2, 4)
    elif event == "-CLOSE PIN-":
        if values["-CLOSE PIN-"]:
            close_pin(4)
            changeState(3, 1)
        else:
            close_pin(5)
            changeState(4, 1)
        open_pin(2)
    
    w, frame = webCam.calculateDistance()

    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    window["-IMAGE-"].update(data=imgbytes)

    if window["-COLPROCESS-"].visible:
        if w >= 350 and not calling_speech:
            close_pin(2)
            open_pin(3)
            changeState(1, 2)
            calling_speech = True
            createThread()
            print('in a range. call speech_recognition function')
        else:
            print(f'not in range. w = {w}')

