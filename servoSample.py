import odroid_wiringpi as wpi
import time
import softPwm

SERVO_PIN = 1

#code om servo op "nul" te zetten




#for loop in python (kuttaal) die van -500 naar 500 gaat met stappen van +2; 180 graden naar links

#servoSpin = 0
#for servoSpin in range(-500, 500, 2):
#     wpi.pwmWrite(SERVO_PIN, servoSpin)
#     time.sleep(0.03)
#     print(servoSpin)
#for loop die van 500 naar -500 gaat in stappen van -1; 180 graden naar rechts
#for servoSpin in range (500, -500, -1):
#     wpi.pwmWrite(SERVO_PIN, servoSpin)
#     time.sleep(0.03)
#     print(servoSpin)

#wpi.softPwmCreate(SERVO_PIN, 50, 100)

#print ("I work!")

# use 'GPIO naming'
wpi.wiringPiSetupGpio()

# set pin 18 to be a PWM output
wpi.pinMode(1, wpi.GPIO.PWM_OUTPUT)

# set the PWM mode to milliseconds style
wpi.pwmSetMode(wpi.PWM_MODE_MS)

delay_period = 0.01

# move servo to 0 degrees
wpi.pwmWrite(1, 0)
time.sleep(delay_period)

# move servo to 90 degrees
wpi.pwmWrite(1, 150)
time.sleep(delay_period)

# move servo to 180 degrees
wpi.pwmWrite(1, 300)
time.sleep(delay_period)

# move servo back to 0 degrees
wpi.pwmWrite(1, 0)
time.sleep(delay_period)
