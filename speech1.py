# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from pyfirmata import Arduino, OUTPUT, INPUT, util
import time
import pyttsx3

# TODO subject to change accroding to personal setting
port = "/dev/cu.usbmodem143401" # Need change
pin = 13
board = Arduino(port)

trigger_pin = 2
echo_pin = 3
led_pin = 13
HIGH = 1
LOW = 0
board = Arduino(port)

board.digital[trigger_pin].mode = OUTPUT
board.digital[echo_pin].mode = INPUT
board.digital[led_pin].mode = OUTPUT


board.digital[pin].mode = OUTPUT

def light_on(pin):
    board.digital[pin].write(1)
    time.sleep(0.015)

def light_off(pin):
    board.digital[pin].write(0)
    time.sleep(0.015)

while(True):
    board.digital[trigger_pin] = HIGH
    time.sleep(0.00001)
    board.digital[trigger_pin] = LOW

    pulse_duration = board.digital[echo_pin].pulse_read()

    distance = pulse_duration * 34300 / 2

    if distance <= 10:
        # obtain audio from the microphone
        engine = pyttsx3.init()
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            engine.say("Say something")
            engine.runAndWait()
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, phrase_time_limit=3)

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text = r.recognize_google(audio, language='en-in')
            print("Google Speech Recognition thinks you said " + text)
            if (text == "open the door"):
                print("door is open!!")
                engine.say("door is open")
                engine.runAndWait()
                light_on(pin)
            elif (text == "close the door"):
                print("door is closed!!")
                engine.say("door is closed")
                engine.runAndWait()
                light_off(pin)
        except sr.UnknownValueError:
            engine.say("Google Speech Recognition could not understand audio")
            print("I cannot undersatand")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

# noicse cancellation
# trigger proximity-ultra sonic / run the program
# open for 30 seconds...