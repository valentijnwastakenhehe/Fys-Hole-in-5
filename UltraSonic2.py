import odroid_wiringpi as wpi
import time

TRIG = 7
ECHO = 8

print("Ultra sonic metingen")

wpi.wiringPiSetup()
wpi.pinMode(TRIG, wpi.OUTPUT)
wpi.pinMode(ECHO, wpi.INPUT)

def distance():

    wpi.digitalWrite(TRIG, wpi.HIGH)

    time.sleep(0.00001)
wpi.digitalWrite(TRIG, wpi.LOW)

start = time.time()
stop = time.time()

print("Debug")

while wpi.digitalRead(ECHO) == 0:
   start = time.time()
   print("Debug0")
while wpi.digitalRead(ECHO) == 1:
   stop = time.time()
   print("Debug1")

elapsed = stop-start

afstand = elapsed * 34300

afstand = afstand / 2
return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print("Gemeten afstand = ", afstand)

print("Afstand = ", afstand)
