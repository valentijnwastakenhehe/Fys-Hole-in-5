import odroid_wiringpi as wpi
import time
import smbus
from playsound import playsound
from pygame import mixer
import pygame
import threading
import pickle

try:
    with open("High_score.dat", "rb") as f:
        high_score.dat = pickle.load(f)
except:
    high_score = 0

I2C_ADDR = 0x27
LCD_WIDTH = 16
LCD_CHR = 1
LCD_CMD = 0

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
LCD_LINE_3 = 0x94
LCD_LINE_4 = 0xD4

LCD_BACKLIGHT = 0x08
ENABLE = 0b00000100

E_PULSE = 0.0005
E_DELAY = 0.0005

bus = smbus.SMBus(0)

# gpio voor led als laser wordt onderbroken. LDR om licht te meten.
LED_PIN1 = 1
LED_PIN2 = 1
LED_PIN3 = 1
LED_PIN4 = 1
LED_PIN5 = 1
LDR_PIN1 = 1
LDR_PIN2 = 1
LDR_PIN3 = 1
LDR_PIN4 = 1
LDR_PIN5 = 1

# gpio voor infrarood sensor
PIR_PIN = 3

wpi.wiringPiSetup()
# Functie voor led als laser wordt onderbroken. LDR om licht te meten.
wpi.pinMode(LED_PIN1, wpi.OUTPUT)
wpi.pinMode(LED_PIN2, wpi.OUTPUT)
wpi.pinMode(LED_PIN3, wpi.OUTPUT)
wpi.pinMode(LED_PIN4, wpi.OUTPUT)
wpi.pinMode(LED_PIN5, wpi.OUTPUT)
wpi.pinMode(LDR_PIN1, wpi.INPUT)
wpi.pinMode(LDR_PIN2, wpi.INPUT)
wpi.pinMode(LDR_PIN3, wpi.INPUT)
wpi.pinMode(LDR_PIN4, wpi.INPUT)
wpi.pinMode(LDR_PIN5, wpi.INPUT)

# Functie voor infrarood.
wpi.pinMode(PIR_PIN, wpi.INPUT)


def infrarood_sensor():
    print("PIR test")
    time.sleep(2)
    wpi.digitalWrite(LED_PIN, wpi.LOW)
    print("Ready")

    while True:
        time.sleep(1)

        if wpi.digitalRead(PIR_PIN) == 1:
                wpi.digitalWrite(LED_PIN, wpi.HIGH)

                print("Odroid hot")
        else:
                wpi.digitalWrite(LED_PIN, wpi.LOW)

                print ("Odroid cold")


def lcd_byte(bits,mode):
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    bus.write_byte(I2C_ADDR, bits_high)

     lcd_toggle_enable(bits_high)
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byt(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(E_DELAY)

def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LDC_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

def handle_high_score():
    global high_score

    if os.path.exists("highscore.txt"):
        f = open("highscore.txt", "r")

        high_score = int(f.read())

        f.close()

def play_audio_files(audio_files):
    for audio_file in audio_files:
        mixer.music.load(audio_file)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)

def countdown(t):

    while t:
      mins, secs = divmod(t, 60)
        timer = '{:02s}:{:02d}'.format(mins,secs)
        lcd_string(timer, LCD_LINE_1)
        lcd_string(" ", LCD_LINE_2)
        time.sleep(1)
        t -= 1
        countdown_finished = True

def start(x):
    mixer.init()
    mixer.music.load("/root/it101-3/Audio/3_2_1.mp3")
    mixer.music.play()
    while x:

        mins, secs = divmod(x, 60)
        timer = '{:02s}:{:02d}'.format(mins,secs)
        lcd_string(timer, LCD_LINE_1)
        lcd_string(" ", LCD_LINE_2)
        time.sleep(1)
        t -= 1

def menu():
    lcd_init()
    mixer.init()
    mixer.music.load("/root/it101-3/Audio/3_2_1.mp3")
    mixer.music.play()
    text = "    welkom"

    for i, c in enumerate(text):
        lcd_string(text[:i+1], LCD_LINE_1)
        time.sleep(0.2)

    time.sleep(0.5)

    text2 = "bij balgooien"
    for i, c in enumerate(text2):
        lcd_string(text2[:i+1], LCD_LINE_2)
        time.sleep(0.2)
        time.sleep(10)
        lcd_string("Game mode", LCD_LINE_1)
        lcd_string("Easy or Hard", LCD_LINE_2)

def niveau():
        global t
    mode = int(input("1 = makkelijk, 2 = moelijk: "))
    if mode == 1:
        t = 60
        lcd_sting("Easy mode", LCD_LINE_1)
        lcd_sting("is selected", LCD_LINE_2)

        lcd_sting("Hard mode", LCD_LINE_1)
        lcd_sting("is selected", LCD_LINE_2)

        mixer.music.stop()
    else:
        print("error")


def game_play():
    LDR_SCORE1 = 0
    LDR_SCORE2 = 0
    LDR_SCORE3 = 0
    LDR_SCORE4 = 0
    LDR_SCORE5 = 0

    pre_ldr1_value = wpi.digitalRead(LDR_PIN1)

    mixer.init()
    mixer.music.load("/root/it101-3/Audio/mariokart.mp3")
    mixer.music.play()
    try:
        with open("high_score.dat", "rb") as f:
            high_score = pickle.load(f)
    except:
        high_score = 0

    countdown_thread = threading.Thread(target=countdown, args=(int(t),))
    countdown_thread.start()

    while t:
        ldr1_value = wpi.digitalRead(LDR_PIN1)
        wpi.digitalRead(LDR_PIN1)
        time.sleep(0.125)
        current_time = time.time()
        elapsed_time = current_time - star_time
        ldr2_value = wpi.digitalRead(LDR_PIN2)

               if pre_ldr1_value == 1 and ldr1_value == 0:
            ldr1_value == wpi.digitalRead(LDR_PIN1)
            wpi.digitalWrite(LED_PIN1, wpi.HIGH)
            LDR_SCORE1 += 50
            print(50)
        pre_ldr1_value = ldr1_value
        time.sleep(0.125)

        if elasped_time > t:
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
                audio_files.append("/root/it101-3/Audio/you_suck.wav")
                audio_files.append("/root/it101-3/Audio/boxing2.mp3")
                threads = []
                p = threading.Thread(target=play_audio_files, args=(audio_files,))
                threads.append(p)

                for p in threads:
                    p.start()
                time.sleep(2)


                print("\nGame over! \n\nJouw score is:", TOTAAL_SCORE)
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
    menu()
    niveau()
    time.sleep(5)
    x=3
    start(x)
    lcd_string("       START", LDC_LINE_1)
    time.sleep(1)
    start_time = time.time()
    game_play()
    infrarood_sensor()
