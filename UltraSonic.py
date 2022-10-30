import odroid_wiringpi as wpi
import time

int GPIO_TRIG = 8 #3
int GPIO_ECHO = 7 #7

print("Ultra sonic metingen")

wpi.wiringPiSetup()
wpi.pinMode(GPIO_TRIG, wpi.OUTPUT)
wpi.pinMode(GPIO_ECHO, wpi.INPUT)

wpi.wiringPiSetup()
wpi.pinMode(TRIG, wpi.OUTPUT)
wpi.pinMode(ECHO, wpi.INPUT)

stop = time.time()

wpi.digitalWrite(TRIG, wpi.LOW)

time.sleep(0.5)
wpi.digitalWrite(TRIG, wpi.HIGH)
time.sleep(0.00001)
wpi.digitalWrite(TRIG, wpi.LOW)
start = time.time()

print("Debug")

while wpi.digitalRead(ECHO) == 0:
   start = time.time()
   print("Debug0")
while wpi.digitalRead(ECHO) == 1:
   stop = time.time()
   print("Debug1")


aftelTijd = stop-start

afstand = aftelTijd * 34300

afstand = afstand / 2

print(afstand)
