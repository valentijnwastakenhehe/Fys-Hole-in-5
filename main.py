import odroid_wiringpi as wpi
import time
import smbus
import datetime
from flask import Flask, render_template
import threading
import mysql.connector

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
BEAM_5 = 3
BEAM_10 = 21
BEAM_15 = 22
BEAM_20 = 23
BEAM_25 = 24

# Flask for webserver
app = Flask(__name__, template_folder='templates')

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
wpi.pinMode(BEAM_5, wpi.INPUT)
wpi.pinMode(BEAM_10, wpi.INPUT)
wpi.pinMode(BEAM_15, wpi.INPUT)
wpi.pinMode(BEAM_20, wpi.INPUT)
wpi.pinMode(BEAM_25, wpi.INPUT)

#### Ultrasonic + database
# connectie met database
def connect_to_database():
    database = mysql.connector.connect(
        host="oege.ie.hva.nl",
        user="bruggev",
        password="#bnbpLjKr6L8mx",
        database="zbruggev"
    )
    return database

# Ultrasonic data naar database versturen
def ultrasonicData(cursor, database, final_afstand):
    database = connect_to_database()  # functie connect_to_database wordt gebruikt om verbinding te maken met database
    cursor = database.cursor()
    distanceTimestamp = datetime.datetime.now()
    sql = "INSERT INTO ultrasonic (timestamp, distance) VALUES (%s, %s)" #stop de variable distance en timestamp in de tabel breakBeam
    val = (distanceTimestamp, final_afstand)
    cursor.execute(sql, val)
    database.commit()

# pak data uit de tabel ultrasonic op de database
def get_ultrasonic_data(cursor):
    ultrasonic_query = "SELECT timestamp, distance FROM ultrasonic"
    cursor.execute(ultrasonic_query)
    return cursor.fetchall()

# functie om een lijst te creëren van de tabel ultrasonic 
def ultrasonicHTMLTable(result):
    p = []
    tbl = "<tr><th>Timestamp</th><th>Distance</th></tr>"
    p.append(tbl)
    for row in result:
        a = "<tr><td>%s</td>"%row[0]
        p.append(a)
        b = "<td>%s</td></tr>"%row[1]
        p.append(b)
    return ''.join(p)

# functie om een html file te creëren
def write_to_file(contents, filename):
    with open(filename, 'w') as f:
        f.write(contents)

# functie om de html file te maken met ultrasonic data uit de database
def ultrasonicTable():
    database = connect_to_database()
    cursor = database.cursor()
    result = get_ultrasonic_data(cursor)
    contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
    <head>
    <meta content="text/html; charset=ISO-8859-1"
    http-equiv="content-type">
    <title>Ultrasonic data</title>
    <style>
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    </style>
    </head>
    <body>
    <table>
      <caption> Distance and timestamp </caption>
    %s
    </table>
    </body>
    </html>
    ''' % ultrasonicHTMLTable(result)
    filename = 'templates/ultrasonic.html'
    write_to_file(contents, filename)
    cursor.close()
    database.close()

##
#  Ultrasonic metingen nemen
def Ultrasonic ():
    # assign variable final_afstand to 1000
    final_afstand = 1000
    # loop tot dat aftsnad < is dan 60
    while final_afstand > 60:
        database = connect_to_database()
        cursor = database.cursor()
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
    # functie aanroepen om data in database op te slaan
    ultrasonicData(cursor, database, final_afstand)

#### Knoppen en servo
## servo; 
def move_servo(start, end, step):
    for servoSpin in range(start, end, step): # for loop met start en eind punt  en snelheid
        wpi.pwmWrite(SERVO_PIN, servoSpin)
        time.sleep(0.08)
#        print(servoSpin)
    time.sleep(0.2)

## Knoppen
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

#### Website control
## Servo
def easy_mode():
    for servoSpin in range(305, 500, 2):
        wpi.pwmWrite(SERVO_PIN, servoSpin)
        time.sleep(0.08)
    return "easy mode"

def medium_mode():
    for servoSpin in range(500, 305, -2):
        wpi.pwmWrite(SERVO_PIN, servoSpin)
        time.sleep(0.08)
    return "medium mode"

def hard_mode():

    for servoSpin in range(305, 110, -2):
        wpi.pwmWrite(SERVO_PIN, servoSpin)
        time.sleep(0.08)
    return "hard mode"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/easy')
def easy():
    return easy_mode()

@app.route('/medium')
def medium():
    return medium_mode()

@app.route('/hard')
def hard():
    return hard_mode()

## Tabellen
# breakbeam tabel
@app.route('/breakBeam')
def breakBeam():
    return render_template('breakBeam.html')

# Ultrasonic tabel
@app.route('/ultrasonic')
def ultrasonic():
    return render_template('ultrasonic.html')

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
# functie om text en een variable te printen op lijn 1 van LCD
def LCD_Your_Score(var):
    lcd_init()
    message = str('Your score:') + ' ' +str(var)
    lcd_string(message, LCD_LINE_1)
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

#### Break beam data
# Break beam data versturen naar database
def breakBeamData(cursor, database, score):
    database = connect_to_database()  # functie connect_to_database wordt gebruikt om verbinding te maken met database
    cursor = database.cursor()
    scoreTimestamp = datetime.datetime.now()
    sql = "INSERT INTO breakBeam (timestamp, score) VALUES (%s, %s)" #stop de variable score en timestamp in de tabel breakBeam
    val = (scoreTimestamp, score)
    cursor.execute(sql, val)
    database.commit()

# Break beam data uit database halen en in tabel op website zetten
def get_break_beam_data(cursor): #functie die de tabel data returned
    break_beam_query = """SELECT timestamp, score FROM breakBeam""" # Pak alle data uit de tabel breakBeam
    cursor.execute(break_beam_query)
    return cursor.fetchall()

# functie die een list variable opslaat om een tabel in html te creëren met kopjes te returnen
def breakBeamHTMLTable(result):
    p = []
    tbl = "<tr><th>Timestamp</th><th>Score</th></tr>"
    p.append(tbl)
    for row in result:
        a = "<tr><td>%s</td>"%row[0]
        p.append(a)
        b = "<td>%s</td></tr>"%row[1]
        p.append(b)
    return ''.join(p)

#functie om een file aan te maken voor een html tabel
def write_to_file(contents, filename):
    with open(filename, 'w') as f:
        f.write(contents)

#functie die data van een database omzet naar een tabel op een website
def breakBeamTable():
    database = connect_to_database()
    cursor = database.cursor()
    result = get_break_beam_data(cursor)
    contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
    <head>
    <meta content="text/html; charset=ISO-8859-1"
    http-equiv="content-type">
    <title>Break beam data</title>
    <style> 
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    </style>
    </head>
    <body>
    <table>
      <caption> Score and timestamp </caption>
    %s
    </table>
    </body>
    </html>
    ''' % breakBeamHTMLTable(result)
    filename = 'templates/breakBeam.html'
    write_to_file(contents, filename)
    cursor.close()
    database.close()

####
# Countdown, scoren bijhouden en naar LCD sturen functie
def gameplay(secondes):
    start_tijd = datetime.datetime.now()
    eind_tijd = start_tijd + datetime.timedelta(seconds=secondes)
    global score
    score = 0
    database = connect_to_database()
    cursor = database.cursor()
    while datetime.datetime.now() < eind_tijd:
        resterend_tijd = eind_tijd - datetime.datetime.now()
        LCDvars('Time:', resterend_tijd.seconds,'Score:', score)
        beams = {BEAM_5: 5, BEAM_10: 10, BEAM_15: 15, BEAM_20: 25, BEAM_25: 25} # Dictionary om break beam score en definitie op te slaan 
        for beam, beam_score in beams.items(): # loop door de dictionary beams met key en value (score en definitie)
            if wpi.digitalRead(beam) == wpi.LOW: # beam is de key
                score += beam_score # beam_score is de value
                # Stuur data van break beam sensor naar database
                breakBeamThread = threading.Thread(target=breakBeamData, args=(cursor, database, score)) # thread van breakbeam om data naar database te versturen
                breakBeamThread.start()

####
# Play again function
def playAgain():
    button_state_easy = wpi.digitalRead(EASY_BUTTON_PIN)
    if button_state_easy == wpi.LOW: # EASY_BUTTON_PIN zit op een SDA die een ingebouwde >
        LCDvar2('Lets try again!', 'Try to beat', score)
        time.sleep(2)
        global pressed
        pressed = 1

def main():
    while True:
        # Ultrasoinc
        Ultrasonic()
        ultrasonicTable()
        # LCD, with wait times
        LCD_Start(2, 0.8)
        # Define variables
        global pressed
        pressed = 0
        global score
        score = 0
        # LCD message to select mode
        LCD_Input('Select Mode!!', ' ')
        # Loop to continuously look for a signal from a button
        while pressed == 0:
            # Scan buttons and move servo
            easyMode()
            mediumMode()
            hardMode()
        # Get input from break beam sensors, keep score and time
        gameplay(tijd)
        # Create a table on website from breakbeam database
        breakBeamTable()
        if score < 70:
            LCDvar1('Score:', score, 'Keep trying!')
            time.sleep(5)
        elif score >= 70 and score < 400:
            LCDvar1('Score:', score, 'Young padawan')
            time.sleep(5)
        else:
            LCDvar1('Score:', score, 'Sensei')
            time.sleep(5)
        LCD_Input('Play again?', 'Press green!!')
        pressed = 0
        while pressed == 0:
            playAgain()
        lcd_byte(0x01, LCD_CMD)

####
# Code runnen
# Handling keyboard interrupts and exception utility
if __name__ == '__main__':

    # Thread to run website along with rest of code
    servo_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 4009})
    

    try:
        servo_thread.start()
        main()

    except KeyboardInterrupt:
        # website stoppen als programma gestopt wordt
        servo_thread.join()
    finally:
        # LCD leeg halen
        lcd_byte(0x01, LCD_CMD)
