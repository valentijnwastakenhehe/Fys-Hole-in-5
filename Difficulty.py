#Deze code is nog niet klaar, een start voor de difficulty button
import odroid_wiringpi as wpi
import time


PUSH_BUTTON_PIN = 0


wpi.wiringPiSetup()


wpi.pinMode(PUSH_BUTTON_PIN, wpi.INPUT)


while True:
    #If button is pressed once print easy, if button is pressed again print hard. If button is pressed again print east etc.
    button_state = wpi.digitalRead(PUSH_BUTTON_PIN)
    while button_state == wpi.HIGH:
        wpi.digitalRead(PUSH_BUTTON_PIN)
        if button_state == wpi.LOW:
            print("Difficulty: Easy")
        while button_state == wpi.HIGH:
            wpi.DigitalRead(PUSH_BUTTON_PIN)
            if button_state == wpi.LOW:
                print ("Difficulty: Hard")
        

           
            time.sleep(0.2)
