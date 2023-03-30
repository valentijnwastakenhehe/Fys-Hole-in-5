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
    print("Easy button state: ", button_state_easy)
    print("Medium button state: ", button_state_medium)
    print("Hard button state: ", button_state_hard)
    time.sleep(1)
    if button_state_easy == wpi.LOW:
        print("Easy mode")
        print("Easy state pressed: ", button_state_easy)
        time.sleep(1)
    if button_state_medium == wpi.HIGH:
        print("Medium mode")
        print("Medium state pressed: ", button_state_medium)
        time.sleep(1)
    if button_state_hard == wpi.LOW:
        print("Hard mode")
        print("Hard state pressed: ", button_state_hard)
        time.sleep(1)

