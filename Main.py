from syslog import LOG_WARNING
from tracemalloc import start
import odroid_wiringpi as wpi
import time
from multiprocessing import process

LED_PIN1 = 7 						#GPIO PIN 7,9
LED_PIN2 = 30 						#GPIO PIN 27,30
LDR_PIN1 = 8 						#GPIO PIN 1,6,3
LDR_PIN2 = 9 						#GPIO PIN 17,20,5
wpi.wiringPiSetup()
wpi.pinMode(LED_PIN1, wpi.OUTPUT)	#Line 12 t/m 15 bind de variables op Lines 7 t/m 10 
wpi.pinMode(LED_PIN2, wpi.OUTPUT)	#aan de WPI waarden van de GPIO pins op de Odroid
wpi.pinMode(LDR_PIN1, wpi.INPUT)	
wpi.pinMode(LDR_PIN2, wpi.INPUT)	
LDR_SCORE1 = 0						#LDR_SCORE1 en 2 zijn de standaard waarde van de score die de speler heeft opgebouwd 
LDR_SCORE2 = 0						#Die we later weer kunnen printen op het scherm
LDR_DELAY1 = 0
LDR_DELAY2 = 0


start_tijd = time.time()			#Bind de variable start_tijd aan de huidige tijd
secondes = 10						#Hoelang het spel duurt kan aangepast worden 


while True:		
	time.sleep(0.06)				#Hoelang de sensor wacht om weer een waarde te geven 
	huidige_tijd = time.time()		#Bind de variable huidige_tijd aan de huidige tijd
	verstreken_tijd = huidige_tijd - start_tijd		#Berekend de verstreken tijd 

	if wpi.digitalRead(LDR_PIN1) == 1:				#Line 31 t/m 33 Als de LDR een positief signaal geeft 
		wpi.digitalWrite(LED_PIN1, wpi.HIGH)		#telt de loop 1 bij LDR_DELAY1 op 
		LDR_DELAY1 += 1								#
	
	else:							#Als de waarde van de LDR niet positief is doet de loop 
		LDR_DELAY2 += 0				#niks met de variable 

	if LDR_DELAY1 > 5:				#
		LDR_SCORE1 += 50			#
		LDR_DELAY1 = 0				#
	else:
		wpi.digitalWrite(LED_PIN1,wpi.LOW)
	
	#if wpi.digitalRead(LDR_PIN2) == 1:
	#	wpi.digitalWrite(LED_PIN2, wpi.HIGH)
	#	LDR_DELAY2 += 1
	
	#else:
	#	LDR_DELAY2 += 0

	#if LDR_DELAY2 > 5:
	#	LDR_SCORE2 += 20
	#	LDR_DELAY2 = 0
	#else:
	#	wpi.digitalWrite(LED_PIN1,wpi.LOW)
	
	if verstreken_tijd > secondes:										#Als de verstreken tijd groter is dan ingestelde tijd  
		TOTAAL_SCORE = LDR_SCORE1 + LDR_SCORE2							#dan eindigt het spel en word je score weergegeven
		print("\nGame over! \n\nJouw score is:" , TOTAAL_SCORE , "\n")	#
		break															#

	#OUD SYSTEEM VOOR PUNTEN BEREKENEN
	#if wpi.digitalRead(LDR_PIN2) == 1:
	#	wpi.digitalWrite(LED_PIN2, wpi.HIGH)
	#	LDR_SCORE2 += 20
	#else:
	#	wpi.digitalWrite(LED_PIN2, wpi.LOW)
	#
	#if wpi.digitalRead(LDR_PIN2) == 1:
	#	wpi.digitalWrite(LED_PIN2, wpi.HIGH)
	#	LDR_SCORE2 += 20
	#else:
	#	wpi.digitalWrite(LED_PIN2, wpi.LOW)
	#
	
		