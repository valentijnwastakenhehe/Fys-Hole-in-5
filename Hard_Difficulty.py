import odroid_wiringpi as wpi
import time

HARD_BUTTON_PIN = 9 #gpio 5 & 6

wpi.wiringPiSetup()

wpi.pinMode(HARD_BUTTON_PIN, wpi.INPUT)



while True:
    #If button is pressed once print hard.
    button_state = wpi.digitalRead(HARD_BUTTON_PIN)
    if button_state == wpi.LOW:
        print("Hard")
        time.sleep(0.2)
