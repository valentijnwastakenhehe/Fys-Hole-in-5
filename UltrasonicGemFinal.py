import odroid_wiringpi as wpi
import time

TRIG = 7
ECHO = 0
LED = 2

wpi.wiringPiSetup()
wpi.pinMode(TRIG, wpi.OUTPUT)
wpi.pinMode(ECHO, wpi.INPUT)
wpi.pinMode(LED, wpi.OUTPUT)

wpi.digitalWrite(LED, wpi.LOW)

def Ultrasonic ():
    # take an average
    while True:
        afstanden = []
        for i in range(10):
            # send a xxSecond pulse to the TRIG pin
            wpi.digitalWrite(TRIG, wpi.HIGH)
            time.sleep(0.00001)
            wpi.digitalWrite(TRIG, wpi.LOW)
            #Wait for the ECHO pin to go HIGH
            while wpi.digitalRead(ECHO) == 0:
                pass
            #Record start time
            start = time.time()
            #Wait for the ECHO pin to go low
            while wpi.digitalRead(ECHO) == 1:
                pass
            #Record the stop time
            stop = time.time()
            afstand = (stop - start)*17150
            afstanden.append(afstand)

        final_afstand = sum(afstanden) / len(afstanden)
        print("Afstand: = ", final_afstand, "cm")

        if final_afstand < 50:
            wpi.digitalWrite(LED, wpi.HIGH)
        else:
            wpi.digitalWrite(LED, wpi.LOW)
while True:
    Ultrasonic()
