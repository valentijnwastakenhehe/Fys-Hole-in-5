import odroid_wiringpi as wpi
import time

SERVO_PIN = 1
EASY_BUTTON_PIN = 8 #gpio 3 & 6(gnd)
MEDIUM_BUTTON_PIN = 9 #gpio 5 & 6(gnd)
HARD_BUTTON_PIN = 12 #gpio 19 & 6(gnd)


#pinnen instellen
wpi.wiringPiSetup()
wpi.pinMode(SERVO_PIN, wpi.PWM_OUTPUT) #set servo pin 1 to output
wpi.pinMode(EASY_BUTTON_PIN, wpi.INPUT) #set easy to pin 8
wpi.pinMode(MEDIUM_BUTTON_PIN, wpi.INPUT) #set medium to pin 9
wpi.pinMode(HARD_BUTTON_PIN, wpi.INPUT) #set hard to pin 12


def easy_mode():
     while True:
          #If button is pressed once select mode easy
          button_state_easy = wpi.digitalRead(EASY_BUTTON_PIN)
          if button_state_easy == wpi.LOW:



easy_mode()
     #for loop die van 500 naar 110 gaat met stappen van -2; 180 graden naar links
     servoSpin = 110
     for servoSpin in range(110, 500, 2):
          wpi.pwmWrite(SERVO_PIN, servoSpin)
          time.sleep(0.08)
          print(servoSpin)
     time.sleep(0.2)
     print ("Easy mode")



