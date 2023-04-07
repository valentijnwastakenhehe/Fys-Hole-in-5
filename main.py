import odroid_wiringpi as wpi
import time
import smbus

# Ultrasonic
TRIG = 7
ECHO = 0

# LCD 
I2C_ADDR = 0x27  # I2C device address
LCD_WIDTH = 16  # Maximum characters per line

# Define device constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

LCD_BACKLIGHT = 0x08  # On
ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Open I2C interface
bus = smbus.SMBus(0)  # Open I2C interface for ODROID-N2+

# Knoppen
EASY_BUTTON_PIN = 30 #fysiek 27 (SDA.3)
MEDIUM_BUTTON_PIN = 6 #fysiek 22 (10K weerstand voor pulldown)
HARD_BUTTON_PIN = 31 #fysiek 28 (SCL.3)

# servo
SERVO_PIN = 1 #12 fysiek (pwm)

# Setup pin modes
wpi.wiringPiSetup()

# Ultrasonic
wpi.pinMode(TRIG, wpi.OUTPUT)
wpi.pinMode(ECHO, wpi.INPUT)

# Knoppen
wpi.pinMode(EASY_BUTTON_PIN, wpi.INPUT) 
wpi.pinMode(MEDIUM_BUTTON_PIN, wpi.INPUT) 
wpi.pinMode(HARD_BUTTON_PIN, wpi.INPUT)

# servo
wpi.pinMode(SERVO_PIN, wpi.PWM_OUTPUT)
 
# functie om Ultrasonic metingen in te stellen
def Ultrasonic ():
    # assign variable final_afstand to 1000
    final_afstand = 1000
    # loop until afstand is smaller then 50
    while final_afstand > 60:
	# take an average
        afstanden = []
        for i in range(10):
            # send a xxSecond pulse to the TRIG pin
            wpi.digitalWrite(TRIG, wpi.HIGH)
            time.sleep(0.00001)
            wpi.digitalWrite(TRIG, wpi.LOW)
            #Wait for the ECHO pin to go HIGH
            while wpi.digitalRead(ECHO) == 0:
                pass
            #Record start time
            start = time.time()
            #Wait for the ECHO pin to go low
            while wpi.digitalRead(ECHO) == 1:
                pass
            #Record the stop time
            stop = time.time()
            afstand = (stop - start)*17150
            afstanden.append(afstand)

        final_afstand = sum(afstanden) / len(afstanden)
#        print("Afstand: = ", final_afstand, "cm")

 #       if final_afstand < 60:
  #          print("Select mode")

####
# code om LCD scherm in te stellen en output te genereren
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


# Set text on display, 
# Initialize display
def LCD_Welcome():
    lcd_init()
    lcd_string('Welcome to', LCD_LINE_1)
    lcd_string('Hole in 5!', LCD_LINE_2)

    time.sleep(6)
    # Send text to I2C
    while True:
        lcd_string("Select mode:", LCD_LINE_1)
        lcd_string("Easy", LCD_LINE_2)

        time.sleep(2)

        lcd_string("Medium", LCD_LINE_2)

        time.sleep(2)

        lcd_string("Hard", LCD_LINE_2)

        time.sleep(2)

#### 
# Knoppen en servo
def move_servo(start, end, step):
    for servoSpin in range(start, end, step):
        wpi.pwmWrite(SERVO_PIN, servoSpin)
        time.sleep(0.08)
        print(servoSpin)
    time.sleep(0.2)

#while True:
     #Check button state and move servo easy mode
 ##   if button_state_easy == wpi.LOW:
   #       move_servo(305, 500, 2)
    #      print("Easy mode")
     #     pressed = 1

     #Check button state and move servo to medium mode
#     button_state_medium = wpi.digitalRead(MEDIUM_BUTTON_PIN)
#     if button_state_medium == wpi.HIGH:
#          move_servo(500, 305, -2)
#          print("Medium mode")
#          pressed = 1
     
     #Check button state and move servo to hard mode
#     button_state_hard = wpi.digitalRead(HARD_BUTTON_PIN)
#     if button_state_hard == wpi.LOW:
#          move_servo(305, 110, -2)
#          print("Hard mode")
#          pressed = 1

####
# Run code 
# Handling keyboard interrupts and exception utility
if __name__ == '__main__':

    try:
        # Ultrasoinc
        Ultrasonic ()
        # LCD wlcome message and select mode
        LCD_Welcome ()
        # Buttons and servo
        pressed = 0
        while pressed == 0:
            #Check button state and move servo easy mode
            button_state_easy = wpi.digitalRead(EASY_BUTTON_PIN)
            if button_state_easy == wpi.LOW:
                move_servo(305, 500, 2)
                print("Easy mode")
                pressed = 1

            #Check button state and move servo to medium mode
            button_state_medium = wpi.digitalRead(MEDIUM_BUTTON_PIN)
            if button_state_medium == wpi.HIGH:
                move_servo(500, 305, -2)
                print("Medium mode")
                pressed = 1
     
            #Check button state and move servo to hard mode
            button_state_hard = wpi.digitalRead(HARD_BUTTON_PIN)
            if button_state_hard == wpi.LOW:
                move_servo(305, 110, -2)
                print("Hard mode")
                pressed = 1
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)

