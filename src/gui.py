import PySimpleGUI as sg

CIRCLE = '⚫'
CIRCLE_OUTLINE = '⚪'

def LED(color, key):
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

window = sg.Window("***Open Sesame Application***", layout, size=(1800, 1400))
