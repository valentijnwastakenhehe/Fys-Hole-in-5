import odroid_wiringpi as wpi
import time

LASER_PIN = 0
LDR_PIN1 = 7
wpi.wiringPiSetup()
wpi.pinMode(LDR_PIN1, wpi.INPUT)
#wpi.pinMode(LDR_PIN2, wpi.INPUT)
wpi.pinMode(LASER_PIN, wpi.OUTPUT)
while True:
        wpi.digitalWrite(LASER_PIN, wpi.HIGH)
        ldr_value = wpi.digitalRead(LDR_PIN1)
        time.sleep(0.25)
        print("ldr  value before if loop: ", ldr_value)
        if wpi.digitalRead(LDR_PIN1) == 1:
#                wpi.digitalWrite(LED_PIN1, wpi.HIGH)
                print('RAAK!1')
                print(ldr_value)
#else:
  #              wpi.digitalWrite(LED_PIN1, wpi.LOW)

#        if wpi.digitalRead(LDR_PIN2) ==1:
 ##               wpi.digitalWrite(LED_PIN2, wpi.HIGH)
   #             print('RAAK!2')
    #    else:
     #           wpi.digitalWrite(LED_PIN2, wpi.LOW)
