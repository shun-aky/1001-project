# NOTE: this script requires PyAudio since it uses the Microphone class
# NOTE: this script also needs mpg321 to play audio files (mp3s)

import speech_recognition as sr             # for speech recognition
# pyfirmata is not supported for Python 3.11. Only till 3.10
from pyfirmata import Arduino, OUTPUT, util # for communication between this mac and arduino
from time import sleep
import os
from mpyg321.MPyg123Player import MPyg123Player

# constant
port ="/dev/cu.usbserial-1430"
pin = 13
pin1 = 1
pin2 = 2
pin3 = 3
pin4 = 4
pin5 = 5

# initialization
player = MPyg123Player()

# if we use pyfirmata
board = Arduino(port)
board.digital[pin].mode = OUTPUT
r = sr.Recognizer()

def open_pin(pin_num):
    board.digital[pin_num].write(0)
    #sleep(1)

def close_pin(pin_num):
    board.digital[pin_num].write(1)
    #sleep(1)    

def light_on():
    # if we use pymata4
    # board.digital_write(pin, 1)
    # if we use pyfirmata
    board.digital[pin].write(1)
    sleep(1)

def light_off():
    # if we use pymata4
    # board.digital_write(pin, 0)
    # if we use pyfirmata
    board.digital[pin].write(0)
    sleep(1)

def speech_recognition():
    light_off()
    # obtain audio from the microphone
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print('start listening')
        
        # os.system("mpg321 src/welcome_words.mp3")
        player.play_song("src/welcome_words.mp3")
        audio = r.listen(source, phrase_time_limit=5)
        print("Say something!")
        # This is path sensitive, which means I have to run this code in 1001-project directory
        print('finish listening')

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print('start recognizing')
        text = r.recognize_google(audio, language='en-us')
        print("Google Speech Recognition thinks you said " + text)
        if (text == "open the door"):
            print("door is open!!")
            # os.system("mpg321 src/success1.mp3")
            player.play_song("src/success1.mp3")
            light_on()
            return True
        elif (text == "close the door"):
            print("door is closed!!")
            # os.system("mpg321 src/success2.mp3")
            player.play_song("srdcsuccess2.mp3")
            light_off()
            return True
        return False
    except sr.UnknownValueError:
        print("I cannot undersatand")
        return False
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        print("This is at our fault")
        print("I will open the door but just this time")
        return True

if __name__ == '__main__':
    while(True):
        speech_recognition()
