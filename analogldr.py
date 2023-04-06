import odroid_wiringpi as wpi
import time

laser_pin = 0
ldr_pin = 29
wpi.wiringPiSetup()
wpi.pinMode(laser_pin, wpi.OUTPUT)
#wpi.pinMode(ldr_pin, wpi.INPUT)

# Turn on laser to set "normal" reading
wpi.digitalWrite(laser_pin, wpi.HIGH)
normal_reading = wpi.analogRead(ldr_pin)

# Continuously monitor LDR voltage
threshold = 100 # Adjust this value to suit your needs
while True:
    voltage = wpi.analogRead(ldr_pin)
    if voltage < normal_reading - threshold:
        # Something has interrupted the laser beam
        print("Object detected!, voltage = ", voltage)
        time.sleep(1)
        # Take appropriate action here, such as sounding an alarm or triggering a camera
    else:
        # Laser beam is unobstructed
        print("Laser beam unobstructed, normal reading = ", normal_reading)
        time.sleep(1)
