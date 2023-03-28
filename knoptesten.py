import odroid_wiringpi as wpi

GREEN__EASY_BUTTON = 0 #11 physical
PURPLE_MEDIUM_BUTTON = 2 #13 physical
RED_HARD_BUTTON = 3 #15 physical

wpi.wiringPiSetup()
wpi.pinMode(PURPLE_MEDIUM_BUTTON, wpi.INPUT)

while True:
# check button state 
    button_state_medium = wpi.digitalRead(PURPLE_MEDIUM_BUTTON)
    if button_state_medium == wpi.LOW:
        print("Medium mode")
