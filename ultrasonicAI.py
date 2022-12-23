import time
import RPi.GPIO as GPIO

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set the trigger and echo pins for the ultrasonic sensor
TRIG = 23
ECHO = 24

# Set the trigger and echo pins as output and input, respectively
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Set the trigger to low
GPIO.output(TRIG, False)

# Wait for the sensor to settle
time.sleep(2)

# Set the trigger to high for 10 microseconds to trigger the ultrasonic pulse
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

# Measure the pulse duration
while GPIO.input(ECHO) == 0:
    pulse_start = time.time()
while GPIO.input(ECHO) == 1:
    pulse_end = time.time()

# Calculate the distance based on the speed of sound and the pulse duration
pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150
distance = round(distance, 2)

# Print the distance
print("Distance:", distance, "cm")

# Clean up the GPIO settings
GPIO.cleanup()
