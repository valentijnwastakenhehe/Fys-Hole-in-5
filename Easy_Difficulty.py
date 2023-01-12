import odroid_wiringpi as wpi
import time

EASY_BUTTON_PIN = 9 #gpio 5 & 6

wpi.wiringPiSetup()

wpi.pinMode(EASY_BUTTON_PIN, wpi.INPUT)



while True:
    #If button is pressed once print easy.
    button_state = wpi.digitalRead(EASY_BUTTON_PIN)
    if button_state == wpi.LOW:
        print("easy")
        time.sleep(0.2)
