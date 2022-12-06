import odroid_wiringpi as wpi
import time
import smbus

# Apparaatparameters definiëren
I2C_ADDR = 0x27
LCD_WIDTH = 16 # Maximum aantal tekens per regel

# Definieer apparaatconstanten
LCD_CHR = 1 # Mode - Data sturen
LCD_CMD = 0 # Mode - Commandos sturen

# Ram addressen voor line 1 t/m 4 
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
#LCD_LINE_3 = 0x94
#LCD_LINE_4 = 0xD4

LCD_BACKLIGHT = 0x08 
ENABLE = 0b00000100 

# Constanten voor timing
E_PULSE = 0.0005
E_DELAY = 0.0005

# I2C interface openen
bus = smbus.SMBus(0)

# WPI waarden van de GPIO pinnen op de Odroid 
LED_PIN1 = 7
LED_PIN2 = 30
#LED_PIN3 = 0    # Nog geen GPIO pin aangewezen
#LED_PIN4 = 0    # Nog geen GPIO pin aangewezen
#LED_PIN5 = 0    # Nog geen GPIO pin aangewezen
LDR_PIN1 = 15
LDR_PIN2 = 16
#LDR_PIN3 = 0    # Nog geen GPIO pin aangewezen
#LDR_PIN4 = 0    # Nog geen GPIO pin aangewezen
#LDR_PIN5 = 0    # Nog geen GPIO pin aangewezen

# GPIO pinnen als input of output configureren  
wpi.wiringPiSetup()
wpi.pinMode(LED_PIN1, wpi.OUTPUT)
wpi.pinMode(LED_PIN2, wpi.OUTPUT)
#wpi.pinMode(LED_PIN3, wpi.OUTPUT)      # Kijk comment line 32
#wpi.pinMode(LED_PIN4, wpi.OUTPUT)
#wpi.pinMode(LED_PIN5, wpi.OUTPUT)
wpi.pinMode(LDR_PIN1, wpi.INPUT)
wpi.pinMode(LDR_PIN2, wpi.INPUT)
#wpi.pinmode(LDR_PIN3, wpi.INPUT)
#wpi.pinmode(LDR_PIN4, wpi.INPUT)
#wpi.pinmode(LDR_PIN5, wpi.INPUT)

# Basis score voor het spel
LDR_SCORE1 = 0
LDR_SCORE2 = 0

# Display Initialiseren
def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(E_DELAY)

# Bytes naar de pins sturen
def lcd_byte(bits, mode):
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    bus.write_byte(I2C_ADDR, buts_high)
    lcd_toggle_enable(bits_high)

    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

# Display klaar maken
def lcd_toggle_enable(bits):
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(E_DELAY)

# Strings naar het display sturen
def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

# Countdown functie 
def countdown(t):
    
    while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{02d}'.format(mins, secs)
            lcd_string(timer, LCD_LINE_1)
            time.sleep(1)
            t -= 1

t = 10  # tijd die het spel duurt 

start_tijd = time.time()    # start_tijd gelijk stellen aan de klok op je laptop   

# Main loop van het spel 
while True:
    wpi.digitalRead(LDR_PIN1) # Niet zeker of dit nodig is
    wpi.digitalRead(LDR_PIN2) # Niet zeker of dit nodig is 
    time.sleep(0.125) # Niet zeker of dit nodig is         
    countdown(int(t)) # Countdown Initialiseren
    huidige_tijd = time.time() # huidige_tijd gelijk stellen aan klok op je laptop
    verstreken_tijd = huidige_tijd - start_tijd # berekening om het spel te eindige wanneer de ingestelde tijd om is
    signal_new1 = wpi.digitalRead(LDR_PIN1)
    signal_new2 = wpi.digitalRead(LDR_PIN2)

    if signal_new1 == 1 and signal_old == 0:
        wpi.digitalWrite(LED_PIN1, wpi.HIGH)
        LDR_SCORE1 += 50
    else:
        wpi.digitalWrite(LED_PIN1, wpi.LOW)
        signal_old = signal_new1
    
    if signal_new2 == 1 and signal_old == 0:
        wpi.digitalWrite(LED_PIN2, wpi.HIGH)
        LDR_SCORE2 += 20
    else:
        wpi.digitalWrite(LED_PIN2, wpi.LOW)
        signal_old = signal_new2
    
    if elapsed_time > t:
        TOTAAL_SCORE = LDR_SCORE1 + LDR_SCORE2
        
        lcd_init()
        
        lcd_string("Game over!", LCD_LINE_1)
        lcd_string(" ", LCD_LINE_2)

        time.sleep(3)

        lcd_string("Jouw Score is:", LCD_LINE_1)
        lcd_string(str(TOTAAL_SCORE), LCD_LINE_2)
        
        time.sleep(3)
        

#def main():
#    lcd_init()
#
#    while True:
#        lcd_string("GAME OVER!", LCD_LINE_1)
#        lcd_string(" ", LCD_LINE_2)
#
#        time.sleep(3)
#
#        lcd_string("Jouw score is:" LCD_LINE_1)
#        lcd_string(str(TOTAAL_SCORE), LCD_LINE_2)
#
#        time.sleep(3)
#
#        if __name__ == '__main__':
#        
#           try:
#               main()
#           except KeyboardInterrupt:
#               pass
#           finally:
#               lcd_byte(0x01, LCD_CMD)
