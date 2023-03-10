import time
from pymata4 import pymata4
import subprocess

trigpin = 2
ecopin = 3

board = pymata4.Pymata4()

def the_callback(data):
    print("distance: ", data[2])
    if data[2] < 100:
        subprocess.call(['python3', '/Users/yaya/Desktop/speech_recognition/speech.py'])
    else:
        print("distance: ", data[2])


board.set_pin_mode_sonar(trigpin, ecopin, the_callback)
while True:
    try:
        time.sleep(0.1)
        board.sonar_read(trigpin)
    except Exception:
        board.shutdown()
