import odroid_wiringpi as wpi
import time

LED_PIN = 9
PIR_PIN = 3

wpi.wiringPiSetup()
#pin 9 is output
wpi.pinMode(LED_PIN, wpi.OUTPUT)
#pin 23 is input
wpi.pinMode(PIR_PIN, wpi.INPUT)

#some print to see if it works
print ("PIR Module Test (CTRL+C to exit)")
time.sleep(2)
print ("Ready")

#check input status of PIR_PIN
while True:
#    wpi.digitalRead(PIR_PIN)
    time.sleep(1)

    if wpi.digitalRead(PIR_PIN) == 1:
            wpi.digitalWrite(LED_PIN, wpi.HIGH)
            print ("Motion Detected!")
    else:
            wpi.digitalWrite(LED_PIN, wpi.LOW)
            print ("No Motion Detected!")


