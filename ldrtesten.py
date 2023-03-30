import odroid_wiringpi as wpi
import time

LDR_PIN1 = 7
wpi.pinMode(LDR_PIN1, wpi.INPUT)
wpi.pinMode(LDR_PIN2, wpi.INPUT)

while True:
        wpi.digitalRead(LDR_PIN1)
        time.sleep(0.25)

        if wpi.digitalRead(LDR_PIN1) == 1:
                wpi.digitalWrite(LED_PIN1, wpi.HIGH)
                print('RAAK!1')
        else:
                wpi.digitalWrite(LED_PIN1, wpi.LOW)

        if wpi.digitalRead(LDR_PIN2) ==1:
                wpi.digitalWrite(LED_PIN2, wpi.HIGH)
                print('RAAK!2')
        else:
                wpi.digitalWrite(LED_PIN2, wpi.LOW)
