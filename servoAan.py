import odroid_wiringpi as wpi
import time

#

START_BUTTON_PIN = 0
SERVO_PIN = 1

wpi.wiringPiSetup()
#pin 0 is input
wpi.pinMode(START_BUTTON_PIN, wpi.INPUT)
#pin 1 is output
wpi.pinMode(SERVO_PIN, wpi.PWM_OUTPUT)

while True:
#what is the state of the button	
     start_button = wpi.digitalRead(START_BUTTON_PIN) 

     if start_button == wpi.HIGH:
         #for loop in python (kuttaal) die van -500 naar 500 gaat met stappen van +2
         servoSpin = 0
         for servoSpin in range(-500, 500, 2):
         wpi.pwmWrite(SERVO_PIN, servoSpin)
         time.sleep(0.03)
         print(servoSpin)

     else:
         #for loop die van 500 naar -500 gaat in stappen van -1
         for servoSpin in range (500, -500, -1):
         wpi.pwmWrite(SERVO_PIN, servoSpin)
         time.sleep(0.03)
         print(servoSpin)

#wait 200ms
     time.sleep(0.2)


