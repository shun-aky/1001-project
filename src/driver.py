# NOTE: https://www.pysimplegui.org/en/latest/cookbook/#recipe-long-operations-multi-threading iw a helpful link for threading

# NOTE: import libraries
import PySimpleGUI as sg
import threading
# from speech import speech_recognition

# NOTE: This is for test
# import cv2
import time

# NOTE: import other py files
# import webcam

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

def LED(color, key):
    """
    A "user defined element".  In this case our LED is based on a Text element. This gives up 1 location to change how they look, size, etc.
    :param color: (str) The color of the LED
    :param key: (Any) The key used to look up the element
    :return: (sg.Text) Returns a Text element that displays the circle
    """
    return sg.Text(CIRCLE_OUTLINE, text_color=color, key=key)

initial_page = [
    [sg.Text("Start Application")],
    [sg.Button("Start", size=(20, 2))]
]

image_viewer = [
    [sg.Text("TEST DEMO")],
    [sg.Image(key="-IMAGE-")],
]

stage_indicator = [
    [sg.Text("Default"), LED("Red", "-LED1-")],
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

window = sg.Window("Open Sesame Application", layout, location=(800, 400))

def switchUIinStarting(turnOn: bool):
    window["-COLINIT-"].update(visible=not turnOn)
    window["-COLPROCESS-"].update(visible=turnOn)
    window["Stop"].update(visible=turnOn)

def changeState(fromState: int, toState: int):
    window[f'-LED{fromState}-'].update(CIRCLE_OUTLINE)
    window[f'-LED{toState}-'].update(CIRCLE)

def functionInThread(window: sg.Window):
    time.sleep(5)
    # if speech_recognition():
    #     print("The door is open")
    #     window.write_event_value('-SPEECH DONE-', '')
    #         # call a function that opens the door
    # else:
    #     if speech_recognition():
    #         print("The door is open this time")
    #     else:
    #         print("Come back later")
    #     print('You\'re in a range!! after speech_recognition')
    #     continue
    window.write_event_value('-THREAD DONE-', '')

def createThread():
    threading.Thread(target=functionInThread, args=(window, ), daemon=True).start()

# webCam = webcam.WebCamera()
w = 100
while True:
    event, values = window.read(timeout=20)
    window['-LED1-'].update(CIRCLE)

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "Start":
        switchUIinStarting(True)
        print("BEFORE")
        createThread()
        print("AFTER")
    elif event == "Stop":
        print("IN STOP")
        switchUIinStarting(False)
    elif event == "-THREAD DONE-":
        print("Function DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
    # w, frame = webCam.calculateDistance()

    # imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    # window["-IMAGE-"].update(data=imgbytes)

    if window["-COLPROCESS-"].visible:
        w += 1
        if w >= 350 and not calling_speech:
            changeState(1, 2)
            print("BEFORE")
            createThread()
            print("AFTER")
            print('You\'re in a range!! before speech_recognition')
            # CREATE THREAD
            # if speech_recognition():
            #     print("The door is open")
            #         # call a function that opens the door
            # else:
            #     if speech_recognition():
            #         print("The door is open this time")
            #     else:
            #         print("Come back later")
            #     print('You\'re in a range!! after speech_recognition')
            #     continue
        else:
                print(f'not in range. w = {w}')


# TODO:
# Initialize parameters
# webCamera = webcam.WebCamera()

