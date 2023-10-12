# NOTE: import libraries
import PySimpleGUI as sg

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
    [sg.Text(f"STAGE 1 "), LED("Red", "-LED1-")],
    [sg.Text(f"STAGE 2 "), LED("Red", "-LED2-")],
    [sg.Text(f"STAGE 3 "), LED("Red", "-LED3-")],
    [sg.Text(f"STAGE 4 "), LED("Red", "-LED4-")]
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
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    try:
        d, frame = webCam.calculateDistance()
    except:
        # TODO:
        # This is when the camera can't detect the face
        continue

    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    window["-IMAGE-"].update(data=imgbytes)

# TODO:
# Initialize parameters
# webCamera = webcam.WebCamera()

