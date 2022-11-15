from syslog import LOG_WARNING
from tracemalloc import start
import odroid_wiringpi as wpi
import time
from multiprocessing import process

LED_PIN1 = 7  # GPIO PIN 7,9
LED_PIN2 = 30  # GPIO PIN 27,30
LDR_PIN1 = 8  # GPIO PIN 1,6,3
LDR_PIN2 = 9  # GPIO PIN 17,20,5
wpi.wiringPiSetup()

wpi.pinMode(LED_PIN1, wpi.OUTPUT)
wpi.pinMode(LED_PIN2, wpi.OUTPUT)
wpi.pinMode(LDR_PIN1, wpi.INPUT)
wpi.pinMode(LDR_PIN2, wpi.INPUT)
LDR_SCORE1 = 0
LDR_SCORE2 = 0
start_tijd = time.time()
secondes = 4


while True:
    if wpi.digitalRead(LDR_PIN1) == 1:
        print(1)
    else:
        print(0)
    time.sleep(0.125)
    #huidige_tijd = time.time()
    #verstreken_tijd = huidige_tijd - start_tijd
    
    

    #if wpi.digitalRead(LDR_PIN1) == 1:
     #   wpi.digitalRead(LDR_PIN1)
      #  while wpi.digitalRead(LDR_PIN1) == 1:
       #     wpi.digitalRead(LDR_PIN1)
        #    if wpi.digitalRead(LDR_PIN1) == 0:
         #       wpi.digitalRead(LDR_PIN1)
          #      LDR_SCORE1 += 50
                
            
               

    #if verstreken_tijd > secondes:
    #    TOTAAL_SCORE = LDR_SCORE1 
    #    print("\nGame over! \n\nJouw score is:", TOTAAL_SCORE, "\n")
        
