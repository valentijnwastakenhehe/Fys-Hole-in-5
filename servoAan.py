import odroid_ wiringPi as wpi
import time

START_BUTTON_PIN = 0

wpi.wiringPi.Setup()
#pin 0 is input
wpi.pinMode(START_BUTTON_PIN, wpi.INPUT)

while True:

    if wpi.digitalRead(START_BUTTON_PIN) == 1:
        print ("Button Pressed!")

    else:
        print("Press the button!")

