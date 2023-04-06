import odroid_wiringpi as wpi
import time

LASER_PIN = 0
LDR_PIN1 = 7
wpi.wiringPiSetup()
#wpi.pinMode(LDR_PIN1, wpi.INPUT)
#wpi.pinMode(LDR_PIN2, wpi.INPUT)
wpi.pinMode(LASER_PIN, wpi.OUTPUT)

wpi.digitalWrite(LASER_PIN, wpi.HIGH)

def rc_time (LDR_PIN1):
    count = 0

    #Output on the pin for 
    wpi.pinMode(LDR_PIN1, wpi.OUTPUT)
    wpi.digitalWrite(LDR_PIN1, wpi.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    wpi.pinMode(LDR_PIN1, wpi.INPUT)

    #Count until the pin goes high
    while (wpi.digitalRead(LDR_PIN1) == wpi.LOW):
        count += 1

    return count

while True:
    print(rc_time(LDR_PIN1))

#while True:
#        wpi.digitalWrite(LASER_PIN, wpi.HIGH)
#        voltage = wpi.digitalRead(LDR_PIN1)
#        time.sleep(0.25)
#        print("ldr  value before if loop: ", laser_on_ldr)
#        if laser_on_ldr > voltage - threshold:
#                wpi.digitalWrite(LED_PIN1, wpi.HIGH)
 #               print('RAAK!1')
#                print(voltage)
#else:
  #              wpi.digitalWrite(LED_PIN1, wpi.LOW)

#        if wpi.digitalRead(LDR_PIN2) ==1:
 ##               wpi.digitalWrite(LED_PIN2, wpi.HIGH)
   #             print('RAAK!2')
    #    else:
     #           wpi.digitalWrite(LED_PIN2, wpi.LOW)
