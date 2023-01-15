import odroid_wiringpi as wpi
import time

TRIG = 7
ECHO = 0
LED = 2

print("Ultra sonic metingen")

wpi.wiringPiSetup()
wpi.pinMode(TRIG, wpi.OUTPUT)
wpi.pinMode(ECHO, wpi.INPUT)
wpi.pinMode(LED, wpi.OUTPUT)
wpi.digitalWrite(LED, wpi.LOW)
while True:

        stop = time.time()
        wpi.digitalWrite(TRIG, wpi.LOW)
        print("Stop: ", stop)

        time.sleep(0.5)
        wpi.digitalWrite(TRIG, wpi.HIGH)
        time.sleep(0.00001)
        wpi.digitalWrite(TRIG, wpi.LOW)
        start = time.time()

        print("Start: ", start)

        print("Debug")

        while wpi.digitalRead(ECHO) == 0:
           start = time.time()
           print("start echo read: ", start)
        while wpi.digitalRead(ECHO) == 1:
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
