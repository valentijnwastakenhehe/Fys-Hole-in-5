from syslog import LOG_WARNING
from tracemalloc import start
import odroid_wiringpi as wpi
import time
from multiprocessing import process

LED_PIN1 = 7 						#GPIO PIN 7,9
LED_PIN2 = 30 						#GPIO PIN 27,30
LED_PIN3 =							#GPIO PIN 						
LDR_PIN1 = 8 						#GPIO PIN 1,6,3
LDR_PIN2 = 9 						#GPIO PIN 17,20,5
LDR_PIN3 = 							#GPIO PIN 
wpi.wiringPiSetup()
wpi.pinMode(LED_PIN1, wpi.OUTPUT)	#Line 12 t/m 15 bind de variables op Lines 7 t/m 10 
wpi.pinMode(LED_PIN2, wpi.OUTPUT)	#aan de WPI waarden van de GPIO pins op de Odroid
wpi.pinMOde(LED_PIN3, wpi.OUTPUT)
wpi.pinMode(LDR_PIN1, wpi.INPUT)	
wpi.pinMode(LDR_PIN2, wpi.INPUT)
wpi.pinMode(LDR_PIN3, wpi.INPUT)	
LDR_SCORE1 = 0						#LDR_SCORE1 en 2 zijn de standaard waarde van de score die
LDR_SCORE2 = 0						#de speler heeft opgebouwd
LDR_SCORE3 = 0						#Die we later weer kunnen printen op het scherm
LDR_SCORE3 = 0						
LDR_DELAY1 = 0
LDR_DELAY2 = 0
LDR_DELAY3 = 0



start_tijd = time.time()			#Bind de variable start_tijd aan de huidige tijd
secondes = 10						#Hoelang het spel duurt kan aangepast worden 


while True:		
	time.sleep(0.06)				#Hoelang de sensor wacht om weer een waarde te geven 
	huidige_tijd = time.time()		#Bind de variable huidige_tijd aan de huidige tijd
	verstreken_tijd = huidige_tijd - start_tijd		#Berekend de verstreken tijd 

	if wpi.digitalRead(LDR_PIN1) == 1:				#Line 39 t/m 41 Als de LDR een positief signaal geeft 
		wpi.digitalWrite(LED_PIN1, wpi.HIGH)		#telt de loop 1 bij LDR_DELAY1 op 
		LDR_DELAY1 += 1								
	
	else:							#Als de waarde van de LDR niet positief is doet de loop 
		LDR_DELAY1 += 0				#niks met de variable 

	if LDR_DELAY1 > 5:				#
		LDR_SCORE1 += 50			#
		LDR_DELAY1 = 0				#
	else:
		wpi.digitalWrite(LED_PIN1,wpi.LOW)
	
	if wpi.digitalRead(LDR_PIN2) == 1:
		wpi.digitalWrite(LED_PIN2, wpi.HIGH)
		LDR_DELAY2 += 1
	
	else:
		LDR_DELAY2 += 0

	if LDR_DELAY2 > 5:
		LDR_SCORE2 += 20
		LDR_DELAY2 = 0
	else:
		wpi.digitalWrite(LED_PIN1,wpi.LOW)
	
	if wpi.digitalRead(LDR_PIN3) == 1:
		wpi.digitalWrite(LED_PIN3, wpi.HIGH)
		LDR_DELAY3 += 1
	
	else:
		LDR_DELAY3 += 0

	if LDR_DELAY3 > 5:
		LDR_SCORE3 += 20
		LDR_DELAY3 = 0
	else:
		wpi.digitalWrite(LED_PIN3,wpi.LOW)
	
	if verstreken_tijd > secondes:										#Als de verstreken tijd groter is dan ingestelde tijd  
		TOTAAL_SCORE = LDR_SCORE1 + LDR_SCORE2 + LDR_SCORE3				#dan eindigt het spel en word je score weergegeven
		print("\nGame over! \n\nJouw score is:" , TOTAAL_SCORE , "\n")	#
		break															#

	

#import odroid_wiringpi as wpi # pyright: ignore[reportMissingImports]
#import time
#
# Hier zijn de GDIO pinnenen hoe de ledjes en LDRs moeten worden aangesloten. 
#LED_PIN1 = 7 #GPIO PIN 7 = + ;9 = -
#LED_PIN2 = 30 #GPIO PIN 27 = +; 30 = +
#LDR_PIN1 = 8 #GPIO PIN m = 1; - = 6; S = 3
#LDR_PIN2 = 9 #GPIO PIN m = 17; - = 20; S = 5
#
# LDR leest iets af daarom is het input. Lampjes worden aangestuurd. Lasers blijven oneindig aan.
#
#wpi.wiringPiSetup()
#wpi.pinMode(LED_PIN1, wpi.OUTPUT)
#wpi.pinMode(LED_PIN2, wpi.OUTPUT)
#wpi.pinMode(LDR_PIN1, wpi.INPUT)
#wpi.pinMode(LDR_PIN2, wpi.INPUT)
#
#LDR_SCORE1 = 0
#LDR_SCORE2 = 0
#
# tijd is geimplementeerd.
# Hij leest de code voor een aantal seconden.
#
#start_time = time.time()
#seconds = 5
#signal_old = 0
#signal_new = 0
#
# Een while-loop voor het continu inlezen van de code. 
# Een time.sleep leest de code over een bepaalde tijd.
# Ervoor zorgen dat elapsed time 0 is en tot een bepaalde tijd telt.
#
#while True:
#	wpi.digitalRead(LDR_PIN1)
#	time.sleep(0.125)
#	current_time = time.time()
#	elapsed_time = current_time - start_time
#
# signal_new om wpi te definieren, omdat het lang is.
# 
# Lampje gaat aan.
# Hij telt 50 punten op bij de score. 
#    signal_new = wpi.digitalRead(LDR_PIN1)
#	if signal_new == 1 and signal_old == 0:
#		wpi.digitalWrite(LED_PIN1, wpi.HIGH)
#		LDR_SCORE1 += 50
#
#	else:
#		wpi.digitalWrite(LED_PIN1, wpi.LOW)
#   	signal_old = signal_new
#
#    signal_newer = wpi.digitalRead(LDR_PIN2)
#	if signal_newer == 1 and signal_old == 0:
#		wpi.digitalWrite(LED_PIN2, wpi.HIGH)
#		LDR_SCORE2 += 20
#	else:
#		wpi.digitalWrite(LED_PIN2, wpi.LOW)
#	   signal_old = signal_newer
#        
# Als aftel tijd hoger is dan aantal secondes,
# Tel dan de scores bij elkaar op.
#
#	if elapsed_time > seconds:
#		TOTAAL_SCORE = LDR_SCORE1 + LDR_SCORE2
#		print("\nGame over! \n\nJouw score is:" , TOTAAL_SCORE)
#		break
#
	
		
