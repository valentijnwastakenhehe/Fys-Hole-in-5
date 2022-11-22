import odroid_wiringpi as wpi
import time

START_BUTTON_PIN = 0
#SERVO_PIN = 

wpi.wiringPiSetup()
#pin 0 is input
wpi.pinMode(START_BUTTON_PIN, wpi.INPUT)

while True:
#what is the state of the button	
     start_button = wpi.digitalRead(START_BUTTON_PIN) 

     if start_button == wpi.HIGH:
        print ("Button Pressed!")

     else:
        print ("Press the button")

#wait 200ms
     time.sleep(0.2)
