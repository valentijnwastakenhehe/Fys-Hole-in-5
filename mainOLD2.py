# -----------------------------------------------------------
# Main python bestand dat ons project laat werken.
# 
#
# (C) 2023
# Author: Sander Hoozemans, Senna Beerens 
# -----------------------------------------------------------

import sqlite3
import odroid_wiringpi as wpi 
import time
import smbus
from playsound import playsound 
from pygame import mixer
import pygame 
import threading
import pickle
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
conn = sqlite3.connect('mainOLD2_data.db')
cursor = conn.cursor()

# Create the database tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS ldr_data (timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ldr1 INTEGER, ldr2 INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS high_scores (ldr_num INTEGER, high_score INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS runs (run_num INTEGER)''')

# Initialize the run count
cursor.execute("INSERT INTO runs (run_num) VALUES (0)")


try:
    with open("high_score.dat", "rb") as f:
        high_score = pickle.load(f)
except:
    high_score = 0


# Apparaatparameters definiëren
I2C_ADDR = 0x27  
LCD_WIDTH = 16  # Maximum aantal tekens per regel

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

def update_high_scores(ldr1_score, ldr2_score):
    cursor.execute("UPDATE high_scores SET high_score = ? WHERE ldr_num = 1", (ldr1_score,))
    cursor.execute("UPDATE high_scores SET high_score = ? WHERE ldr_num = 2", (ldr2_score,))
    conn.commit

def update_run_count():
    cursor.execute("UPDATE runs SET run_num = run_num + 1 WHERE run_num = (SELECT MAX(run_num) FROM runs)")
    conn.commit()

def get_run_count():
    cursor.execute("SELECT run_num FROM runs WHERE run_num = (SELECT MAX(run_num) FROM runs)")
    run_count = cursor.fetchone()[0]
    return run_count

def get_high_scores():
    cursor.execute("SELECT ldr_num, high_score FROM high_scores")
    high_scores = cursor.fetchall()
    return high_scores

def handle_high_score():
    global high_score
    
    # Check if the file exists
    if os.path.exists("highscore.txt"):
        # Open the file to read the high score
        f = open("highscore.txt", "r")

        # Read the high score from the file
        high_score = int(f.read())

        # Close the file
        f.close()

def play_audio_files(audio_files):
    for audio_file in audio_files:
        mixer.music.load(audio_file)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)

# define the countdown func.
def countdown(t):
    
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        lcd_string(timer, LCD_LINE_1)
        lcd_string(" ", LCD_LINE_2)
        time.sleep(1)
        t -= 1

def start(x):
    mixer.init()
    mixer.music.load("/root/it101-3/Audio/3_2_1.mp3")
    mixer.music.play()  
    while x:
 
        mins, secs = divmod(x, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        lcd_string(timer, LCD_LINE_1)
        lcd_string(" ", LCD_LINE_2)
        time.sleep(1)
        x -= 1

def menu():
    lcd_init()
    mixer.init()
    mixer.music.load("/root/it101-3/Audio/Wii_sports.mp3")
    mixer.music.play()
    text = "    welkom"

    # Display the text one character at a time
    for i, c in enumerate(text):
        lcd_string(text[:i+1], LCD_LINE_1)
        time.sleep(0.2)

    time.sleep(0.5)

    text2 = "bij balgooien"
    for i, c in enumerate(text2):
        lcd_string(text2[:i+1], LCD_LINE_2)
        time.sleep(0.2)    
    time.sleep(10)
    lcd_string(" Game mode", LCD_LINE_1)
    lcd_string("Easy or Hard", LCD_LINE_2)

def niveau():
    global t
    mode = int(input(" 1= makkelijk, 2 = moeilijk: "))
    if mode == 1:
        t = 60
        lcd_string("Easy mode", LCD_LINE_1)
        lcd_string("is selected", LCD_LINE_2)
        mixer.music.stop()
    elif mode == 2:
        t = 5
        lcd_string("Hard mode", LCD_LINE_1)
        lcd_string("is selected", LCD_LINE_2)
        mixer.music.stop()
    else:
        print("error")  

def game_play():
    LDR_SCORE1 = 0
    LDR_SCORE2 = 1000
    try:
        with open("high_score.dat", "rb") as f:
            high_score = pickle.load(f)
    except:
        high_score = 0
    while input:
        mixer.init()
        mixer.music.load("/root/it101-3/Audio/mariokart.mp3")
        mixer.music.play()
        wpi.digitalRead(LDR_PIN1)
        time.sleep(0.125)
        countdown(int(t))
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
            
        if elapsed_time > t:
            mixer.music.stop()
            
            TOTAAL_SCORE = LDR_SCORE1 + LDR_SCORE2
            audio_files = []
            audio_files.append("/root/it101-3/Audio/game_over.mp3")
            if TOTAAL_SCORE > high_score:
                audio_files.append("/root/it101-3/Audio/high_score.wav")
                high_score = TOTAAL_SCORE
                with open("high_score.dat", "wb") as f:
                    pickle.dump(high_score, f)
            if TOTAAL_SCORE > 500:
                audio_files.append("/root/it101-3/Audio/you_cheated.wav")
            if TOTAAL_SCORE < 100:
                audio_files.append("/root/it101-3/Audio/you_suck.wav")
            audio_files.append("/root/it101-3/Audio/boxing2.mp3")
            threads = []
            p = threading.Thread(target=play_audio_files, args=(audio_files,))
            threads.append(p)
            
            for p in threads:
                p.start()
            time.sleep(2)



            print("\nGame over! \n\nJouw score is:" , TOTAAL_SCORE)
            start_tijd = time.time()
            while True:

                lcd_string("Jouw score is:", LCD_LINE_1)
                lcd_string(str(TOTAAL_SCORE), LCD_LINE_2)
                    
                time.sleep(3)

                lcd_string("high score is:", LCD_LINE_1)
                lcd_string(str(high_score), LCD_LINE_2)

                time.sleep(3)

                verlopen_tijd = time.time() - start_tijd

                if verlopen_tijd > 15:
                    break
        break


while True:
    get_run_count()
    menu()
    niveau()
    time.sleep(5)
    x=3
    start(x)
    lcd_string("    START", LCD_LINE_2)
    time.sleep(1)
    start_time = time.time()
    game_play()
