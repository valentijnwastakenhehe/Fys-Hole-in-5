import odroid_wiringpi as wpi
import time

MEDIUM_BUTTON_PIN = 9 #gpio 5 & 6

wpi.wiringPiSetup()

wpi.pinMode(MEDIUM_BUTTON_PIN, wpi.INPUT)



while True:
    #If button is pressed once print medium.
    button_state = wpi.digitalRead(MEDIUM_BUTTON_PIN)
    if button_state == wpi.LOW:
        print("medium")
        time.sleep(0.2)

