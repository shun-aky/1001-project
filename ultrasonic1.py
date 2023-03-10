import pyfirmata
import time

# Set up the connection to the Arduino board
board = pyfirmata.Arduino('/dev/cu.usbmodem144301')

# Define the pins used for the ultrasonic sensor
trig_pin = board.get_pin('d:2:o')
echo_pin = board.get_pin('d:3:i')

# Set the trigger pin low to start
trig_pin.write(0)

# Wait for the sensor to settle
time.sleep(2)

# Send a pulse to the sensor
trig_pin.write(1)
time.sleep(0.00001)
trig_pin.write(0)

# Wait for the echo pin to go high
while echo_pin.read() == 0:
    pulse_start = time.time()

# Wait for the echo pin to go low again
while echo_pin.read() == 1:
    pulse_end = time.time()

# Calculate the pulse duration and distance
pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150

# Print the distance in centimeters
print("Distance: %.2f cm" % distance)

# Close the connection to the Arduino board
board.exit()
