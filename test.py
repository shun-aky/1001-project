#!/usr/bin/env python3

from pyfirmata import Arduino, OUTPUT, INPUT
import time

from speech import light_on, light_off

# trigger_pin = 2
# echo_pin = 3
led_pin = 13
HIGH = 1
LOW = 0
port = "/dev/cu.usbserial-1420"
board = Arduino(port)

# board.digital[trigger_pin] = OUTPUT
# board.digital[echo_pin] = INPUT
# board.digital[led_pin] = OUTPUT
pin = board.get_pin(f'd:{led_pin}:o')

while True:
    # board.digital[trigger_pin] = HIGH
    # time.delayMicroseconds(10)
    # board.digital[trigger_pin] = LOW

    # t = time.pulseIn(echo_pin, HIGH)

    # distance = (t * 0.034) / 2

    # if distance <= 10:
    #     print("hello!")
    # board.digital[led_pin] = HIGH
    # time.delay(500)
    # else:
    # board.digital[led_pin] = LOW
    #     time.delay(500)
    # light_off()
    # pin.write(1)
    light_on()
    light_off()
    # print('test is in progress')