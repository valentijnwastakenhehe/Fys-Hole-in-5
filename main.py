import odroid_wiringpi as wpi
import time
import smbus
import datetime

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
## De knoppen zijn verbonden met een sdc, scl en 10k weerstand op normale pin. Dit voorkomt dat de input heen en weer gaat (Hi z)
EASY_BUTTON_PIN = 30 #fysiek 27 (SDA.3)
MEDIUM_BUTTON_PIN = 6 #fysiek 22 (10K weerstand voor pulldown)
HARD_BUTTON_PIN = 31 #fysiek 28 (SCL.3)

# servo
SERVO_PIN = 1 #12 fysiek (pwm)

# Break beam sensor
BEAM_10 = 3

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

#break beam
wpi.pinMode(BEAM_10, wpi.INPUT)
 
# functie om Ultrasonic metingen in te stellen
def Ultrasonic ():
    # assign variable final_afstand to 1000
    final_afstand = 1000
    # loop tot dat aftsnad < is dan 60
    while final_afstand > 60:
	# maak een gemiddelde meting van 10 metingen
        afstanden = []
        for i in range(10):
            # stuur een pulse naar de TRIG pin
            wpi.digitalWrite(TRIG, wpi.HIGH)
            time.sleep(0.00001)
            wpi.digitalWrite(TRIG, wpi.LOW)
            # Wacht tot de echo hoog gaat 
            while wpi.digitalRead(ECHO) == 0:
                pass
            # sla start tijd op
            start = time.time()
            # wacht tot echo pin laag gaat
            while wpi.digitalRead(ECHO) == 1:
                pass
            # sla stop tijd op
            stop = time.time()
            afstand = (stop - start)*17150
            afstanden.append(afstand)

        final_afstand = sum(afstanden) / len(afstanden)

####
## Knoppen en servo
# servo; 
def move_servo(start, end, step):
    for servoSpin in range(start, end, step): # for loop met start en eind punt  en snelheid
        wpi.pwmWrite(SERVO_PIN, servoSpin)
        time.sleep(0.08)
        print(servoSpin)
    time.sleep(0.2)

# Easy knop + servo stand; functie die de knop scant voor een signaal om vervolgens de servo aan te sturen
def easyMode():
    #Check button state and move servo easy mode
    button_state_easy = wpi.digitalRead(EASY_BUTTON_PIN)
    if button_state_easy == wpi.LOW: # EASY_BUTTON_PIN zit op een SDA die een ingebouwde pull up resistor heeft dus als de knop gedrukt is geeft die een een laag signaal
        LCD_Input('Easy mode', 'selected')
        move_servo(305, 500, 2)
        time.sleep(0.2)
        global pressed # global variable aanpassen
        pressed = 1
        global tijd
        tijd = 60
        LCD_Input('60 seconds to', 'play!!')
        time.sleep(1.4)

# Medium knop + servo stand; functie die de knop scant voor een signaal om vervolgens de servo aan te sturen
def mediumMode():
    #Check button state and move servo to medium mode
    button_state_medium = wpi.digitalRead(MEDIUM_BUTTON_PIN)
    if button_state_medium == wpi.HIGH: # MEDIUM_BUTTON_PIN zit op een normale gpio en is aangesloten met een pull down resistordus als de knop gedrukt is geeft die een hoog signaal
        LCD_Input('Medium mode', 'selected')
        move_servo(500, 305, -2)
        time.sleep(0.2)
        global pressed 
        pressed = 1
        global tijd
        tijd = 45
        LCD_Input('45 seconds to', 'play!!')
        time.sleep(1.4)

# Hard knop + servo stand; functie die de knop scant voor een signaal om vervolgens de servo aan te sturen
def hardMode():
    #Check button state and move servo to hard mode
    button_state_hard = wpi.digitalRead(HARD_BUTTON_PIN)
    if button_state_hard == wpi.LOW: # HARD_BUTTON_PIN zit op een SDA die een ingebouwde pull up resistor heeft dus als de knop gedrukt is geeft die een een laag signaal
        LCD_Input('Hard mode', 'selected')
        move_servo(305, 110, -2)
        time.sleep(0.2)
        global pressed
        pressed = 1
        global tijd
        tijd = 30
        LCD_Input('30 seconds to', 'play!!')
        time.sleep(1.4)

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

####
# LCD with own input
def LCD_Input(one, two): # argumenten voor text op regels 1 en 2 van de LCD
    lcd_init()
    lcd_string(str(one), LCD_LINE_1)
    lcd_string(str(two), LCD_LINE_2)
    time.sleep(0.4)
# LCD welcome text and mode options
def LCD_Start(welcomeWait, modeWait): # argumenten voor wachtijd na boodschappen op LCD
    LCD_Input('Welcome to ', 'hole in five!!')
    time.sleep(welcomeWait)
    LCD_Input('Select mode:', 'Easy')
    time.sleep(modeWait)
    LCD_Input('Select mode:', 'Medium')
    time.sleep(modeWait)
    LCD_Input('Select mode:', 'Hard')
    time.sleep(modeWait)
def LCD1(text):
    lcd_init()
    lcd_string(text, LCD_LINE_1)
    time.sleep(2)
# variable and input on line 2
def LCDvar2(one, input, var):
    lcd_init()
    message = str(input) + ' ' + str(var)
    LCD_Input(one, message)
def LCDvar1(input, var, two):
    lcd_init()
    message = str(input) + ' ' + str(var)
    LCD_Input(message, two)
def LCDvars(input1, var1, input2, var2):
    lcd_init()
    message1 = str(input1) + ' ' + str(var1)
    message2 = str(input2) + ' ' + str(var2)
    LCD_Input(message1, message2)
####
# Countdown, scoren bijhouden en naar LCD sturen functie
def gameplay(secondes):
    start_tijd = datetime.datetime.now()
    eind_tijd = start_tijd + datetime.timedelta(seconds=secondes)
    global score
    score = 0
    while datetime.datetime.now() < eind_tijd:
        resterend_tijd = eind_tijd - datetime.datetime.now()
        LCDvars('Time:', resterend_tijd.seconds,'Score:', score)
        beamTen_state = wpi.digitalRead(BEAM_10)
        if beamTen_state == wpi.LOW:
#            print("U scored!")
#            time.sleep(0.5)
#            global score
            score += 10
          #  LCD_Input('Current score', score)
            print(score)
           # time.sleep(1)

####
# Play again function
def playAgain():
    button_state_easy = wpi.digitalRead(EASY_BUTTON_PIN)
    if button_state_easy == wpi.LOW: # EASY_BUTTON_PIN zit op een SDA die een ingebouwde >
        LCDvar2('Lets try again!', 'Try to beat', score)
        time.sleep(2)
        global pressed
        pressed = 1

####
# Main game code 
# Handling keyboard interrupts and exception utility
if __name__ == '__main__':

    try:
        while True:
            # Ultrasoinc
            Ultrasonic ()
            # LCD, with wait times
            LCD_Start(2, 0.8)
            # Define variables
            global pressed
            pressed = 0
            score = 0
            # LCD message to select mode
            LCD_Input(' ', 'Select mode')
            # Loop to continuously look for a signal from a button
            while pressed == 0:
                # Scan buttons and move servo
                easyMode()
                mediumMode()
                hardMode()
            # Get input from break beam sensors, keep score and time
            gameplay(tijd)
            if score < 70:
                LCDvar1('Score:', score, 'Keep trying!')
                time.sleep(3)
            elif score >= 70 and score < 400:
                LCDvar1('Score:', score, 'Young padawan')
                time.sleep(3)
            else:
                LCDvar1('Score:', score, 'Sensei')
                time.sleep(3)
            LCD_Input('Play again?', 'Press easy!!')
            pressed = 0
            while pressed == 0:
                playAgain()
            lcd_byte(0x01, LCD_CMD)

        print('I work son')
        time.sleep(3)
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)

