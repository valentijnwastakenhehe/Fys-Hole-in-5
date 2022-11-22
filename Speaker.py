import odroid_wiringpi as wpi
import time

buzzer_pin = 9  #nummer van pin

wpi.wiringPiSetup()

wpi.pinMode(buzzer_pin, wpi.OUTPUT)

while True:
    wpi.digitalWrite(buzzer_pin, True)
    time.sleep(.3)
    wpi.digitalWrite(buzzer_pin, False)
    time.sleep(.5)

