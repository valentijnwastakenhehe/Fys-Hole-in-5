import odroid_wiringpi as wpi
import time

SERVO_PIN = 1

#set servo pin 1 to output
wpi.wiringPiSetup()
wpi.pinMode(SERVO_PIN, wpi.PWM_OUTPUT)

#code om servo op "nul" te zetten


#for loop in python (kuttaal) die van -500 naar 500 gaat met stappen van +2; 180 graden naar links
servoSpin = 0
for servoSpin in range(-500, 500, 2):
     wpi.pwmWrite(SERVO_PIN, servoSpin)
     time.sleep(0.03)
     print(servoSpin)

#for loop die van 500 naar -500 gaat in stappen van -1; 180 graden naar rechts
for servoSpin in range (500, -500, -1):
     wpi.pwmWrite(SERVO_PIN, servoSpin)
     time.sleep(0.03)
     print(servoSpin)


print ("I work!")

