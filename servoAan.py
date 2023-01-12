import odroid_wiringpi as wpi
import time

SERVO_PIN = 1

#set servo pin 1 to output
wpi.wiringPiSetup()
wpi.pinMode(SERVO_PIN, wpi.PWM_OUTPUT)

#code om servo op "nul" te zetten

def easy_mode():
     #for loop die van 500 naar 110 gaat met stappen van -2; 180 graden naar links
     servoSpin = 500
     for servoSpin in range(500, 110, -2):
          wpi.pwmWrite(SERVO_PIN, servoSpin)
          time.sleep(0.03)
          print(servoSpin)

def medium_mode():
     #for loop die van 500 naar 305 gaat; 90 graden
     servoSpin = 500
     for servoSpin in range (500, 305, -2):
          wpi.pwmWrite(SERVO_PIN, servoSpin)
          time.sleep(0.03)
          print(servoSpin)

def hard_mode():
     #for loop die van 110 naar 500 gaat; 180 graden
     servoSpin = 110
     for servoSpin in range (110, 500, 2);
     wpi.pwmWrite(SERVO_PIN, servoSpin)
     time.sleep(0.03)
     print(servoSpin)

print ("I work!")



