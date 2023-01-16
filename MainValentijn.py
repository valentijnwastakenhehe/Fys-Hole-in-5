# -----------------------------------------------------------
# Main python bestand dat ons project laat werken.
# 
#
# (C) 2023
# Author: Sander Hoozemans, Senna Beerens 
# -----------------------------------------------------------

# Onze imports om het project te laten werken
import odroid_wiringpi as wpi 
import time
import smbus
from playsound import playsound 
from pygame import mixer
import pygame 
import threading
import pickle

# Kijken of het .dat bestand bestaat als het niet zo is high_score = 0 om errors te voorkomen
try:
    with open("high_score.dat", "rb") as f:
        high_score = pickle.load(f)
except:
    high_score = 0


# Apparaatparameters definiëren
I2C_ADDR = 0x27  
LCD_WIDTH = 16  # Maximum aantal tekens per regel
LCD_CHR = 1  # Mode - Data sturen 
LCD_CMD = 0  # Mode - Commandos sturen 

LCD_LINE_1 = 0x80  # LCD RAM adres voor de 1ste lijn
LCD_LINE_2 = 0xC0  # LCD RAM adres voor de 2de lijn
LCD_LINE_3 = 0x94  # LCD RAM adres voor de 3de lijn
LCD_LINE_4 = 0xD4  # LCD RAM adres voor de 4de lijn

LCD_BACKLIGHT = 0x08  # LCD aan
ENABLE = 0b00000100  # Enable bit

# Timing constanten
E_PULSE = 0.0005
E_DELAY = 0.0005

# I2C interface openen
bus = smbus.SMBus(0)  

# GPIO pins hoe de ledjes en LDRs moeten worden aangesloten. 
LED_PIN1 =  1	#GPIO PIN + = '' ; - = '' ;
LED_PIN2 =  1	#GPIO PIN + = '' ; - = '' ;
LDR_PIN1 =  15	#GPIO PIN + = '' ; - = '' ; S = '' ;
LDR_PIN2 =  1	#GPIO PIN + = '' ; - = '' ; S = '' ;
LDR_PIN3 =  1	#GPIO PIN + = '' ; - = '' ; S = '' ;
LDR_PIN4 =  1	#GPIO PIN + = '' ; - = '' ; S = '' ;
LDR_PIN5 =  1	#GPIO PIN + = '' ; - = '' ; S = '' ;

#GPIO van ultrasonic
TRIG = 7 #7 fysiek
ECHO =  #0 fysiek

#GPIO van servo en knoppen
SERVO_PIN = 1 #12 fysiek (oranje op servo, bruin is gnd)
EASY_BUTTON_PIN = 8 #3 fysiek
MEDIUM_BUTTON_PIN = 9 #5 fysiek
HARD_BUTTON_PIN = 30 #27 fysiek

# LDR leest iets af daarom is het input. Lampjes worden aangestuurd. Lasers blijven oneindig aan.
wpi.wiringPiSetup()
wpi.pinMode(LED_PIN1, wpi.OUTPUT)
wpi.pinMode(LED_PIN2, wpi.OUTPUT)
wpi.pinMode(LDR_PIN1, wpi.INPUT)
wpi.pinMode(LDR_PIN2, wpi.INPUT)
wpi.pinMode(LDR_PIN3, wpi.INPUT)
wpi.pinMode(LDR_PIN4, wpi.INPUT)
wpi.pinMode(LDR_PIN5, wpi.INPUT)

#Ultrasonic wiringPiSetup
wpi.pinMode(TRIG, wpi.OUTPUT)
wpi.pinMode(ECHO, wpi.INPUT)

#Servo en knoppen wiringPiSetup
wpi.pinMode(SERVO_PIN, wpi.PWM_OUTPUT)
wpi.pinMode(EASY_BUTTON_PIN, wpi.INPUT)
wpi.pinMode(MEDIUM_BUTTON_PIN, wpi.INPUT)
wpi.pinMode(HARD_BUTTON_PIN, wpi.INPUT)

#Ultrasonic functie
def Ultrasonic ():
    #pak de gemiddelde van 10
    while True:
        afstanden = []
        for i in range(10):
            #pulse van 10 microseconde naar TRIG pin
            wpi.digitalWrite(TRIG, wpi.HIGH)
            time.sleep(0.00001)
            wpi.digitalWrite(TRIG, wpi.LOW)
            #wacht tot echo hoog gaat
            while wpi.digitalRead(ECHO) == 0:
                pass
            #start tijd
            start = time.time()
            #wacht tot echo laag gaat
            while wpi.digitalRead(ECHO) == 1:
                pass
            #stop tijd
            stop = time.time()
            afstand = (stop - start)*17150
            afstanden.append(afstand)

        final_afstand = sum(afstanden) / len(afstanden)
        print("Afstand: = ", final_afstand, "cm")

        if final_afstand < 50:
            wpi.digitalWrite(LED, wpi.HIGH)
        else:
            wpi.digitalWrite(LED, wpi.LOW)


#Servo en knoppen functie
def servo_en_knoppen():
     def move_servo(start, end, step):
          for servoSpin in range(start, end, step):
               wpi.pwmWrite(SERVO_PIN, servoSpin)
               time.sleep(0.08)
               print(servoSpin)
          time.sleep(0.2)

     while True:
          #Check button state and move servo easy mode
          button_state_easy = wpi.digitalRead(EASY_BUTTON_PIN)
          if button_state_easy == wpi.LOW:
               move_servo(305, 500, 2)
               print("Easy mode")

          #Check button state and move servo to medium mode
          button_state_medium = wpi.digitalRead(MEDIUM_BUTTON_PIN)
          if button_state_medium == wpi.LOW:
               move_servo(500, 305, -2)
               print("Medium mode")
     
          #Check button state and move servo to hard mode
          button_state_hard = wpi.digitalRead(HARD_BUTTON_PIN)
          if button_state_hard == wpi.LOW:
               move_servo(305, 110, -2)
               print("Hard mode")


# Display initialiseren
def lcd_init():
    lcd_byte(0x33, LCD_CMD)  # 110011 initialiseren
    lcd_byte(0x32, LCD_CMD)  # 110010 initialiseren
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor beweegt richting
    lcd_byte(0x0C, LCD_CMD)  # 001100 Weergave aan, cursor uit, knipperen uit
    lcd_byte(0x28, LCD_CMD)  # 101000 Gegevens lengte, aantal regels, lettergrootte
    lcd_byte(0x01, LCD_CMD)  # 000001 Display Legen 
    time.sleep(E_DELAY)


# Stuur byte naar datapinnen
# (bits = de data, #mode = 1 voor data of 0 voor commando)
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


# String naar het display sturen
def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)


# Highscore systeem 
def handle_high_score():
    global high_score
    
    # Controleer of het bestand bestaat
    if os.path.exists("highscore.txt"):
        # Open het bestand om de hoogste score te lezen
        f = open("highscore.txt", "r")

        # Lees de hoogste score uit het bestand
        high_score = int(f.read())

        # Sluit het bestand
        f.close()


# Audio systeem 
def play_audio_files(audio_files):
    for audio_file in audio_files:
        mixer.music.load(audio_file)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)


# Countdown systeem
def countdown(t):
    
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        lcd_string(timer, LCD_LINE_1)
        lcd_string(" ", LCD_LINE_2)
        time.sleep(1)
        t -= 1
        countdown_finished = True


# Start audio
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


# Menu audio
def menu():
    lcd_init()
    mixer.init()
    mixer.music.load("/root/it101-3/Audio/Wii_sports.mp3")
    mixer.music.play()
    text = "    welkom"

    # Geef de tekst teken voor teken weer
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


# Moeilijks graad systeem 
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


# Main code
def game_play():
    LDR_SCORE1= 0
    LDR_SCORE2 = 0

    pre_ldr1_value= wpi.digitalRead(LDR_PIN1)

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
        elapsed_time = current_time - start_time
        ldr2_value = wpi.digitalRead(LDR_PIN2)
    
    
        if pre_ldr1_value == 1 and ldr1_value == 0:
            ldr1_value = wpi.digitalRead(LDR_PIN1)
            wpi.digitalWrite(LED_PIN1, wpi.HIGH)
            LDR_SCORE1 += 50
            print(50)
        pre_ldr1_value = ldr1_value
        time.sleep(0.125)
    
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
    menu()
    niveau()
    time.sleep(5)
    x=3
    start(x)
    lcd_string("    START", LCD_LINE_1)
    time.sleep(1)
    start_time = time.time()
    game_play()


