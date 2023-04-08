import odroid_wiringpi as wpi
import time

BEAM_10 = 3

wpi.wiringPiSetup()
wpi.pinMode(BEAM_10, wpi.INPUT)

score = 0

def tenPoints():
    beamTen_state = wpi.digitalRead(BEAM_10)
    print(beamTen_state)
    time.sleep(1)
    if beamTen_state == wpi.LOW:
        print("U scored!")
        time.sleep(0.5)
        global score
        score += 10
        print(score)
        time.sleep(1)
while True:
    tenPoints()
