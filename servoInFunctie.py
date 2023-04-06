import odroid_wiringpi as wpi
import time

SERVO_PIN = 1 #12 fysiek
EASY_BUTTON_PIN = 30 #fysiek 27 (SDA.3)
MEDIUM_BUTTON_PIN = 6 #fysiek 22 (10k weerstand voor pulldown)
HARD_BUTTON_PIN = 31 #fysiek 28 (SCL.3)

#pinnen instellen
wpi.wiringPiSetup()
wpi.pinMode(SERVO_PIN, wpi.PWM_OUTPUT) #set servo pin 1 to output
#set buttons to input
wpi.pinMode(EASY_BUTTON_PIN, wpi.INPUT) 
wpi.pinMode(MEDIUM_BUTTON_PIN, wpi.INPUT) 
wpi.pinMode(HARD_BUTTON_PIN, wpi.INPUT)


def move_servo(start, end, step):
    for servoSpin in range(start, end, step):
        wpi.pwmWrite(SERVO_PIN, servoSpin)
        time.sleep(0.08)
        print(servoSpin)
    time.sleep(0.2)


while True:
     #Check button state and move servo easy mode
     button_state_easy = wpi.digitalRead(EASY_BUTTON_PIN)
     if button_state_easy == wpi.LOW:
          move_servo(305, 500, 2)
          print("Easy mode")

     #Check button state and move servo to medium mode
     button_state_medium = wpi.digitalRead(MEDIUM_BUTTON_PIN)
     if button_state_medium == wpi.HIGH:
          move_servo(500, 305, -2)
          print("Medium mode")
     
     #Check button state and move servo to hard mode
     button_state_hard = wpi.digitalRead(HARD_BUTTON_PIN)
     if button_state_hard == wpi.LOW:
          move_servo(305, 110, -2)
          print("Hard mode")
