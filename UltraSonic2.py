import odroid_wiringpi as wpi
import time

client_loop: send disconnect: Connection reset
ECHO = 8
TRIG = 7

print("Ultra sonic metingen")

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

elapsed = start-stop

afstand = elapsed * 34300

afstand = afstand / 2
print("Afstand = ", afstand)
print("Start = ", start)
print("Stop = ", stop)
print("elapsed = ", elapsed)
print("time = ", time.time)
