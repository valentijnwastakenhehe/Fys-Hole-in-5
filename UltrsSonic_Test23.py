import odroid_wiringpi as wpi
import time

TRIG = 7 #van 23 naar 27 oftewel 33 naar 36 fysiek
ECHO = 0

print("Ultra sonic metingen")

wpi.wiringPiSetup()
wpi.pinMode(TRIG, wpi.OUTPUT)
wpi.pinMode(ECHO, wpi.INPUT)
#wpi.pinMode(LED, wpi.OUTPUT)

while True:

        stop = time.time()
        wpi.digitalWrite(TRIG, wpi.LOW)
        print("Stop at low: ", stop)

        time.sleep(10.5)
        wpi.digitalWrite(TRIG, wpi.HIGH)
        print("now high at trig", stop)
        time.sleep(10.99)
        wpi.digitalWrite(TRIG, wpi.LOW)
        start = time.time()

        print("Start: ", start)

        #print("Debug")

        while wpi.digitalRead(ECHO) == 0:
         pass
         start = time.time()
         #print("start echo read: ", start)
        while wpi.digitalRead(ECHO) == 1:
         pass
         stop = time.time()
         print("Stop echo == 1: ", stop)

        elapsed = stop-start

        print("Stop: ", stop)
        print("Elapsed: ", elapsed)

        afstand = elapsed * 34300

        afstand = afstand / 2

        print("Afstand = ", afstand)

        if afstand < 32:
               wpi.digitalWrite(LED, wpi.HIGH)
        else:
               wpi.digitalWrite(LED, wpi.LOW)
