import odroid_wiringpi as wpi
import time

SERVO_PIN = 1

#set servo pin 1 to output
wpi.wiringPiSetup()
wpi.pinMode(SERVO_PIN, wpi.PWM_OUTPUT)

servoSpin = 0
for servoSpin in range(-500, 500, 2):
     wpi.pwmWrite(SERVO_PIN, servoSpin)
     time.sleep(0.03)
     print(servoSpin)

for servoSpin in range (500, -500, -1):
     wpi.pwmWrite(SERVO_PIN, servoSpin)
     time.sleep(0.03)
     print(servoSpin)

#wpi.softPwmCreate(SERVO_PIN, 50, 100)

print ("I work!")

