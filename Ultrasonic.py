# Gebruikte bron = https://www.raspberrypi-spy.co.uk/2012/12/ultrasonic-distance-measurement-using-python-part-1/

import odroid_wiringpi as wpi
import time

# Trigger pin(andere pinnen werken niet).
# Echo pin(andere pinnen werken niet).
# Ground moet verbazendwekkend op de ground.
# Vcc moet op pin 5.

TRIG = 23 #33
ECHO = 24 #35
LED = 7 # 7 = +; 5 = -

print("Ultra sonic metingen")

# Trigger werkt als een lamp. Dze triggert de Echo.
# Echo leest de waardes in en wordt daarom gebruikt als output.
wpi.wiringPiSetup()
wpi.pinMode(TRIG, wpi.OUTPUT)
wpi.pinMode(ECHO, wpi.INPUT)
wpi.pinMode(LED, wpi.OUTPUT)

# While loop, zodat de waardes constant worden ingelezen.
while True:

# Stop wordt gedefiniëerd.
# Trigger staat eerst uit.
        stop = time.time()
        wpi.digitalWrite(TRIG, wpi.LOW)

# Trigger wordt ingeschakeld over 0.5 sec.

# De trigger heeft puls nodig van 0.00001 sec om te triggeren.

# Start wordt gedefiëerd.
        time.sleep(0.5)
        wpi.digitalWrite(TRIG, wpi.HIGH)
        time.sleep(0.00001)
        wpi.digitalWrite(TRIG, wpi.LOW)
        start = time.time()

# Om te testen.
        print("Debug")

# Als de echo geen waardes inleest blijft de tijd lopen.
        while wpi.digitalRead(ECHO) == 0:
           start = time.time()

# Als de echo wel een waarde inleest stopt de tijd.
        while wpi.digitalRead(ECHO) == 1:
           stop = time.time()

# Leest de tijd in wat het heeft geduurd, vanaf het starten en stoppen van de echo.
        elapsed = stop-start

# De geluidssnelheid die ongeveer 34300 cm/s is wordt keer de elapsed sec gedaan, 
# zodat de afstand in cm wordt uitgerekend.  
        afstand = elapsed * 34300

        afstand = afstand / 2

        print("Afstand = ", afstand)

# Als de afstand kleiner is dan blahblah cm is gaat het lampje aan.

# Zo niet gaat die uit.
        if afstand < 32:
               wpi.digitalWrite(LED, wpi.HIGH)
        else:
               wpi.digitalWrite(LED, wpi.LOW)
