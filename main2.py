import odroid_wiringpi as wpi 
import time
import smbus


# Define device parameters
I2C_ADDR = 0x27  # I2C device address, if any error,
# change this address to 0x3f
LCD_WIDTH = 16  # Maximum characters per line

# Define device constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

LCD_BACKLIGHT = 0x08  # On
ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Open I2C interface
bus = smbus.SMBus(0)  # Open I2C interface for ODROID-C2

#Hier zijn de GDIO pinnenen hoe de ledjes en LDRs moeten worden aangesloten. 
LED_PIN1 = 7 	#GPIO PIN 7 = + ;9 = -
LED_PIN2 = 30 	#GPIO PIN 27 = +; 30 = +
LDR_PIN1 = 15 	#GPIO PIN m = 1; - = 6; S = 8
LDR_PIN2 = 16 	#GPIO PIN m = 17; - = 20; S = 10

# LDR leest iets af daarom is het input. Lampjes worden aangestuurd. Lasers blijven oneindig aan.

wpi.wiringPiSetup()
wpi.pinMode(LED_PIN1, wpi.OUTPUT)
wpi.pinMode(LED_PIN2, wpi.OUTPUT)
wpi.pinMode(LDR_PIN1, wpi.INPUT)
wpi.pinMode(LDR_PIN2, wpi.INPUT)

LDR_SCORE1 = 0
LDR_SCORE2 = 0



# Initialise display
def lcd_init():
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)


# Send byte to data pins
# (#bits = the data, #mode = 1 for data or 0 for command)
def lcd_byte(bits, mode):
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    bus.write_byte(I2C_ADDR, bits_high)  # High bits
    lcd_toggle_enable(bits_high)

    bus.write_byte(I2C_ADDR, bits_low)  # Low bits
    lcd_toggle_enable(bits_low)


# Toggle enable
def lcd_toggle_enable(bits):
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(E_DELAY)


# Send string to display
def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)


# Main program block, # Initialize display


    # Send text to I2C TWI 1602 16x2 Serial LCD Module Display
    


# Handling keyboard interrupts and exception utility




#tijd is geimplementeerd.
#Hij leest de code voor een aantal seconden.



#Een while-loop voor het continu inlezen van de code. 
#Een time.sleep leest de code over een bepaalde tijd.
#Ervoor zorgen dat elapsed time 0 is en tot een bepaalde tijd telt.
#signal_new om wpi te definieren, omdat het lang is.
#Lampje gaat aan.
#Hij telt 50 punten op bij de score.

while True:
	wpi.digitalRead(LDR_PIN1)
	time.sleep(0.125)
	current_time = time.time()
	elapsed_time = current_time - start_time
	signal_new = wpi.digitalRead(LDR_PIN1)
	signal_newer = wpi.digitalRead(LDR_PIN2)
		
	if signal_new == 1 and signal_old == 0:
		wpi.digitalWrite(LED_PIN1, wpi.HIGH)
		LDR_SCORE1 += 50

	else:
			
		wpi.digitalWrite(LED_PIN1, wpi.LOW)
		signal_old = signal_new
		
	
	if signal_newer == 1 and signal_old == 0:
		wpi.digitalWrite(LED_PIN2, wpi.HIGH)
		LDR_SCORE2 += 20
	
	else:
		
		wpi.digitalWrite(LED_PIN2, wpi.LOW)
		signal_old = signal_newer
        
# Als aftel tijd hoger is dan aantal secondes,
# Tel dan de scores bij elkaar op.

	if elapsed_time > seconds:
		TOTAAL_SCORE = LDR_SCORE1 + LDR_SCORE2
		print("\nGame over! \n\nJouw score is:" , TOTAAL_SCORE)
		break

def main():
    lcd_init()

    while True:
        lcd_string("GAME OVER!", LCD_LINE_1)
        lcd_string("Jouw score is:", LCD_LINE_2)

        time.sleep(3)

        lcd_string(TOTAAL_SCORE, LCD_LINE_1)
        lcd_string(TOTAAL_SCORE, LCD_LINE_2)

        time.sleep(3)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)