import odroid_wiringpi as wpi
import time

# set TRIG and ECHO pin numbers
TRIG = 7 #7 fysiek
ECHO = 0 #11 fysiek
LED = 2 #13 fysiek

# initiaize the wiringpi library
wpi.wiringPiSetup()

# Set the TRIG pin as output and ECHO pin as input
wpi.pinMode(TRIG, wpi.OUTPUT)
wpi.pinMode(ECHO, wpi.INPUT)


while True:
    # send a xxSecond pulse to the TRIG pin
        wpi.digitalWrite(TRIG, wpi.HIGH)
        #statement om te testen; print("trig is high now")

        time.sleep(0.00001)
        wpi.digitalWrite(TRIG, wpi.LOW)
        #statement om te testen; print("now low at trig")

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

        print("Afstand: = ", afstand, "cm")

