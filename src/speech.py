# NOTE: this script requires PyAudio since it uses the Microphone class

import speech_recognition as sr             # for speech recognition
# pyfirmata is not supported for Python 3.11. Only till 3.10
from pyfirmata import Arduino # for communication between this mac and arduino
from mpyg321.MPyg123Player import MPyg123Player
import requests
import base64

# constant
port ="/dev/cu.usbserial-1430"
pin1 = 1
pin2 = 2
pin3 = 3
pin4 = 4
pin5 = 5
url = "https://api.github.com/repos/shun-aky/1001-project/contents/keyword.txt"

# initialization
def initialize_speech() -> None:
    global board, recognizer, player
    board = Arduino(port)
    recognizer = sr.Recognizer()
    player = MPyg123Player()
    get_keyword()
    print("Finished initialization in speech.py")

def open_pin(pin_num) -> None:
    global board
    print(f"Open {pin_num}")
    board.digital[pin_num].write(0)

def close_pin(pin_num) -> None:
    global board
    print(f"Close {pin_num}")
    board.digital[pin_num].write(1)

def closeAllPins() -> None:
    for i in range(2, 9):
        close_pin(i)

def get_keyword() -> None:
    global keyword    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.json()["content"]
            content = content.encode("utf-8")
            content = base64.b64decode(content).decode("utf-8")
            keyword = content.split("\n")[0]
            print("Got story successfully: ", keyword)
        else:
            print("Failed to get the story. Status code: ", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Failed to get the story:", str(e))
    except:
        print("Failed to get the story.")

def speech_recognition():
    global keyword, board, recognizer, player
    # obtain audio from the microphone
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print('start listening')
        player.play_song("/Users/newuser/1001++/1001-project/src/welcome_words.mp3")
        audio = recognizer.listen(source, phrase_time_limit=5)
        print("Say something!")
        print('finish listening')

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print('start recognizing')
        text = recognizer.recognize_google(audio, language='en-us')
        print("Google Speech Recognition thinks you said " + text)
        if (text == keyword):
            print("door is open!!")
            player.play_song("/Users/newuser/1001++/1001-project/src/success1.mp3")
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
    initialize_speech()
    while(True):
        speech_recognition()
