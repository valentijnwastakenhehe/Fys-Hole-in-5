from syslog import LOG_WARNING
from tracemalloc import start
import odroid_wiringpi as wpi
import time
from multiprocessing import process

SERVO_PIN = 7 						#GPIO PIN 7,9
KNOP_PIN = 8 						#GPIO PIN 1,6,3
wpi.wiringPiSetup()
wpi.pinMode(SERVO_PIN, wpi.OUTPUT)	#Line 12 t/m 15 bind de variables op Lines 7 t/m 10 	#aan de WPI waarden van de GPIO pins op de Odroid
wpi.pinMode(KNOP_PIN, wpi.INPUT)	