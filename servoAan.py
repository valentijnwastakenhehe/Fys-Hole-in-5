import odroid_wiringpi as wpi
import time

#
#knoppen
EASY_BUTTON_PIN = 0     #gpio11
MEDIUM_BUTTON_PIN = 2   #gpio 13
HARD_BUTTON_PIN = 3     #gpio15

#servo
SERVO_PIN = 1

wpi.wiringPiSetup()

#wpi 0, 2 en 3 zijn input
wpi.pinMode(EASY_BUTTON_PIN, MEDIUM_BUTTON_PIN, HARD_BUTTON_PIN, wpi.INPUT)

#pin 1 is output
wpi.pinMode(SERVO_PIN, wpi.PWM_OUTPUT)

while True:
#what is the state of the button	
     easy_button = wpi.digitalRead(EASY_BUTTON_PIN) 

     print("Push button!") 
     if easy_button == wpi.HIGH:
         #for loop die van -500 naar 500 gaat met stappen van +2; 180 graden naar links
         servoSpin = 0
         for servoSpin in range(500, 2): 
            wpi.pwmWrite(SERVO_PIN, servoSpin)
            time.sleep(0.03)
            print(servoSpin)
         #for loop die van 500 naar -500 gaat in stappen van -1; 180 graden naar rechts
         #for servoSpin in range (500, -1, -1):
         #   wpi.pwmWrite(SERVO_PIN, servoSpin)
          #  time.sleep(0.03)
         ##   print(servoSpin)


#wait 200ms
     time.sleep(0.2)


