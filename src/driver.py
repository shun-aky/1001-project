# NOTE: import libraries
import PySimpleGUI as sg
from speech import speech_recognition

# NOTE: This is for test
import cv2

# NOTE: import other py files
import webcam

# TODO:
# Read a keyword from the repo every week

# NOTE:
# Initialization below

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

image_viewer = [
    [sg.Text("TEST DEMO")],
    [sg.Image(filename="", key="-IMAGE-")],
    [sg.Button("Exit", size=(10, 1))]
]

stage_indicator = [
    [sg.Text("Default"), LED("Red", "-LED1-")],
    [sg.Text("Face Detected"), LED("Red", "-LED2-")],
    [sg.Text("Password Passed"), LED("Red", "-LED3-")],
    [sg.Text("Password Failed - Try Again"), LED("Red", "-LED4-")],
    [sg.Text("Password Failed - Good Bye"), LED("Red", "-LED5-")]
]

layout = [
    [
        sg.Column(image_viewer),
        sg.VSeperator(),
        sg.Column(stage_indicator)
    ]
]
window = sg.Window("Open Sesame Application", layout, location=(800, 400))

webCam = webcam.WebCamera()

while True:
    event, values = window.read(timeout=20)
    window['-LED1-'].update(CIRCLE)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    w, frame = webCam.calculateDistance()

    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    window["-IMAGE-"].update(data=imgbytes)

    if w >= 350:
        window['-LED1-'].update(CIRCLE_OUTLINE)
        window['-LED2-'].update(CIRCLE)
        print('You\'re in a range!! before speech_recognition')
        if speech_recognition():
            print("The door is open")
                # call a function that opens the door
        else:
            if speech_recognition():
                print("The door is open this time")
            else:
                print("Come back later")
            print('You\'re in a range!! after speech_recognition')
            continue
    else:
            print('not in range')
        

# TODO:
# Initialize parameters
# webCamera = webcam.WebCamera()

