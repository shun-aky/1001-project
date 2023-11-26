# NOTE: https://www.pysimplegui.org/en/latest/cookbook/#recipe-long-operations-multi-threading iw a helpful link for threading

# NOTE: import libraries
import cv2
import PySimpleGUI as sg
import threading
import time

# NOTE: import other py files
import constant
from gui import window, CIRCLE_OUTLINE, CIRCLE
from speech import speech_recognition, open_pin, close_pin, closeAllPins, initialize_speech
import webcam

def switchUIinStarting(turnOn: bool) -> None:
    window["-COLINIT-"].update(visible=not turnOn)
    window["-COLPROCESS-"].update(visible=turnOn)
    window["Stop"].update(visible=turnOn)

def changeState(fromState: int, toState: int) -> None:
    window[f'-LED{fromState}-'].update(CIRCLE_OUTLINE)
    window[f'-LED{toState}-'].update(CIRCLE)

def functionInThread(window: sg.Window) -> None:
    right_word = speech_recognition()
    window.write_event_value('-SPEECH DONE-', right_word)
    time.sleep(2)
    window.write_event_value('-CLOSE PIN-', right_word)

def createThread() -> None:
    threading.Thread(target=functionInThread, args=(window, ), daemon=True).start()


def initialize():
    global webCam, calling_speech
    webCam = webcam.WebCamera()
    calling_speech = False
    initialize_speech()
    closeAllPins()
    print("Finished initialization in driver.py")

def main():
    initialize()
    while True:
        global webCam, calling_speech
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
                changeState(2, 3)
                open_pin(4)
            else:
                changeState(2, 4)
                open_pin(5)
        elif event == "-CLOSE PIN-":
            if values["-CLOSE PIN-"]:
                changeState(3, 1)
                close_pin(4)
            else:
                changeState(4, 1)
                close_pin(5)
            open_pin(2)
        
        w, frame = webCam.calculateDistance()

        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

        if window["-COLPROCESS-"].visible:
            if w >= 350 and not calling_speech:
                changeState(1, 2)
                close_pin(2)
                open_pin(3)
                calling_speech = True
                createThread()
                print('in a range. call speech_recognition function')
            else:
                print(f'not in range. w = {w}')

if __name__ == '__main__':
    main()