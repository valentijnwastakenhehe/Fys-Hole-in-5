import odroid_wiringpi as wpi
import time

int GPIO_TRIG = 8 #3
int GPIO_ECHO = 7 #7

print("Ultra sonic metingen")

wpi.wiringPiSetup()
wpi.pinMode(GPIO_TRIG, wpi.OUTPUT)
wpi.pinMode(GPIO_ECHO, wpi.INPUT)

wpi.OUTPUT(GPIO_TRIG, False)

time.sleep(0.5)

wpi.OUTPUT(GPIO_TRIG, True)
time.sleep(0.00001)
wpi.OUTPUT(GPIO_TRIG, False)
start = time.time()

while wpi.INPUT(GPIO_ECHO) == 0:
   start = time.time()

while wpi.INPUT(GPIO_ECHO) == 0:
   stop = time.time()

aftelTijd = stop-start

afstand = aftelTijd * 34300

afstand = afstand / 2

print(afstand)
