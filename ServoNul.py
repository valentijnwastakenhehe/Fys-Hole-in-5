import odroid_wiringpi as wpi
import time

SERVO_PIN = 1

#set servo pin 1 to output
wpi.wiringPiSetup()
wpi.pinMode(SERVO_PIN, wpi.PWM_OUTPUT)

#code om servo op "nul" te zetten

servoSpin = 0
for servoSpin in range (500, 305, -2):
     wpi.pwmWrite(SERVO_PIN, servoSpin)
     time.sleep(0.03)
     print(servoSpin)


print ("I work!")


