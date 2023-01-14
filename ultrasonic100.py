import odroid_wiringpi as wpi
import time

# Set the TRIG and ECHO pin numbers
TRIG = 23 
ECHO = 24 

# Initialize the wiringpi library
wpi.wiringPiSetup()

# Set the TRIG pin as output and ECHO pin as input
wpi.pinMode(TRIG, wpi.OUTPUT)
wpi.pinMode(ECHO, wpi.INPUT)

while True:
    # Send a 10uS pulse to the TRIG pin
    wpi.digitalWrite(TRIG, wpi.HIGH)
    time.sleep(0.00001)
    wpi.digitalWrite(TRIG, wpi.LOW)

    # Wait for the ECHO pin to go high
    while wpi.digitalRead(ECHO) == 0:
        pass

    # Record the start time
    start = time.time()

    #print start time
    print("Start: ", start)

    # Wait for the ECHO pin to go low
    while wpi.digitalRead(ECHO) == 1:
        pass

    # Record the stop time
    stop = time.time()

    #print stop time
    print("Stop: ", stop)

    # Calculate the distance in cm
    distance = (stop - start) * 17150
    
    print("Afstand: ", distance)
