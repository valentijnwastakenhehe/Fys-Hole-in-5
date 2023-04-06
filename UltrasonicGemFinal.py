import odroid_wiringpi as wpi
import time

TRIG = 7
ECHO = 0

wpi.wiringPiSetup()
wpi.pinMode(TRIG, wpi.OUTPUT)
wpi.pinMode(ECHO, wpi.INPUT)

def Ultrasonic ():
    # assign variable final_afstand to 1000
    final_afstand = 1000
    # loop until afstand is smaller then 50
    while final_afstand > 60:
	# take an average
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
#        print("Afstand: = ", final_afstand, "cm")

        if final_afstand < 60:
            print("Select mode")

Ultrasonic()

