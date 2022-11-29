
KNOP_PIN = 8 #GPIO PIN m = 1,- = 6,S = 3
LED_PIN = 7 #GPIO PIN m = 2,- = 9,S = 7
LED_PIN2 = 9 #GPIO PIN m = 4,- = 39,S = 5

# Rode knop = paarse draad: +; groene draad: -
# Rode knop2 = gele draad: +; blauwe draad: -
# Groene knop = oranje draad: +; rode draad: -
# Paarse knop = Rode draad: +; blauwe draad: -

wpi.wiringPiSetup()
wpi.pinMode(KNOP_PIN, wpi.INPUT)
wpi.pinMode(LED_PIN, wpi.OUTPUT)
wpi.pinMode(LED_PIN2, wpi.OUTPUT)

signal_old = 0
signal_new = 0
number = 0

wpi.digitalWrite(LED_PIN, wpi.LOW)
wpi.digitalWrite(LED_PIN2, wpi.LOW)


while True:

    time.sleep(0.1)
    signal_new = wpi.digitalRead(KNOP_PIN)

    if signal_new == 0 and signal_old == 1:
            number += 1

    else:
            signal_old = signal_new


    if number == 1:
            print("Hard")
            wpi.digitalWrite(LED_PIN, wpi.HIGH)
            wpi.digitalWrite(LED_PIN2, wpi.LOW)

    elif number >= 2:
            print("Easy")
            wpi.digitalWrite(LED_PIN, wpi.LOW)
            wpi.digitalWrite(LED_PIN2, wpi.HIGH)

