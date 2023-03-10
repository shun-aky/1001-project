#!/usr/bin/env python3

from pyfirmata import Arduino, OUTPUT, INPUT
from pyfirmata.util import ping_time_to_distance
import time

echo_pin = board.get_pin('d:3:i')
ping_time_to_distance(echo_pin.ping())


trigger_pin = 2
echo_pin = 3
led_pin = 13
HIGH = 1
LOW = 0
port = '/dev/cu.usbmodem144301'
board = Arduino(port)

board.digital[trigger_pin] = OUTPUT
board.digital[echo_pin] = INPUT
board.digital[led_pin] = OUTPUT

while True:
    board.digital[trigger_pin] = HIGH
    time.sleep(0.015)
    board.digital[trigger_pin] = LOW

    t = board.pulseIn(echo_pin, HIGH)

    distance = (t * 0.034) / 2

    if distance <= 10:
        board.digital[led_pin] = HIGH
        time.sleep(0.015)
        print("hello")
    else:
        board.digital[led_pin] = LOW
        time.sleep(0.015)
        print("too far away")
