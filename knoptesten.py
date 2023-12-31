import odroid_wiringpi as wpi
import time

GREEN_EASY_BUTTON = 30 #27 physical
PURPLE_MEDIUM_BUTTON = 6 #22 physical
RED_HARD_BUTTON = 31 #28 physical

wpi.wiringPiSetup()
wpi.pinMode(PURPLE_MEDIUM_BUTTON, wpi.INPUT)

while True:
    # check button state 
    button_state_easy = 0
    button_state_medium = 0
    button_state_hard = 0
    button_state_easy = wpi.digitalRead(GREEN_EASY_BUTTON) # read value of easy pin
    button_state_medium = wpi.digitalRead(PURPLE_MEDIUM_BUTTON) # read the value of medium button 
    button_state_hard = wpi.digitalRead(RED_HARD_BUTTON) # read value of hard button
    if button_state_easy == wpi.LOW:
        print("Easy mode")
        time.sleep(1)
    if button_state_medium == wpi.HIGH:
        print("Medium mode")
        time.sleep(1)
    if button_state_hard == wpi.LOW:
        print("Hard mode")
        time.sleep(1)

