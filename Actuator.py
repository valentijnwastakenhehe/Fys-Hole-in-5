from syslog import LOG_WARNING
from tracemalloc import start
import odroid_wiringpi as wpi
import time
from multiprocessing import process

SERVO_PIN = 7 						#GPIO PIN 7,9
KNOP_PIN = 8 						#GPIO PIN 1,6,3
wpi.wiringPiSetup()
wpi.pinMode(SERVO_PIN, wpi.OUTPUT)	#Line 12 t/m 15 bind de variables op Lines 7 t/m 10 	
wpi.pinMode(KNOP_PIN, wpi.INPUT)	#aan de WPI waarden van de GPIO pins op de Odroid

while True:
    time.sleep(0.1)

    if wpi.digitalRead(KNOP_PIN) == 1:
        print('1')

    else:
        print('0')