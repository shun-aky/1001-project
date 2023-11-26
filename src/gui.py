import PySimpleGUI as sg

CIRCLE = '⚫'
CIRCLE_OUTLINE = '⚪'

def LED(color, key, mark=CIRCLE_OUTLINE) -> sg.Text:
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

column_to_be_centered = [
    [
        sg.Column(initial_page, key='-COLINIT-', element_justification='c'),
        sg.Column(processing_page, key='-COLPROCESS-', visible=False)
    ],
    [sg.Button("Exit", size=(10, 1)), sg.Push(), sg.Button("Stop", visible=False, size=(10, 1))]
]

layout = [
	[sg.VPush()],
    [sg.Push(), sg.Column(column_to_be_centered,element_justification='c'), sg.Push()],
    [sg.VPush()]
]

window = sg.Window("Open Sesame Application", layout, size=(1100, 700), element_justification='c')
