import time
from pymata4 import pymata4
import pyttsx3
import speech_recognition as sr

trigger_pin = 2
eco_pin = 3
led_pin = 13
r = sr.Recognizer()

board = pymata4.Pymata4()
board.set_pin_mode_digital_output(led_pin)

def light_on(pin):
    board.digital_write(pin, 1)
    time.sleep(0.015)

def light_off(pin):
    board.digital_write(pin, 0)
    time.sleep(0.015)

def the_callback(data):
    if data[2] < 10:
        engine = pyttsx3.init()
        print("distance: ", data[2])
        with sr.Microphone() as source:
            print("Say something!")
            engine.say("Say something")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, phrase_time_limit=3)
        try:
            text = r.recognize_google(audio, language='en-in')
            print("Google Speech Recognition thinks you said " + text)
            if (text == "open the door"):
                print("door is open!!")
                engine.say("door is open")
                light_on(led_pin)
            elif (text == "close the door"):
                print("door is closed!!")
                engine.say("door is closed")
                light_off(led_pin)
        except sr.UnknownValueError:
            engine.say("Google Speech Recognition could not understand audio")
            print("I cannot undersatand")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    else:
        print("elseselse ", data[2])

board.set_pin_mode_sonar(trigger_pin, eco_pin, the_callback)

while True:
    try:
        time.sleep(0.1)
        board.sonar_read(trigger_pin)
    except Exception:
        board.shutdown()
