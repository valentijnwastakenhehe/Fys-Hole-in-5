import sqlite3
import odroid_wiringpi as wpi
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
conn = sqlite3.connect('ldr_data.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS ldr_data (timestamp TIMESTAMP, ldr1 INTEGER, ldr2 INTEGER)''')

LED_PIN1 = 7  # GPIO PIN 7,9
LED_PIN2 = 30  # GPIO PIN 27,30
LDR_PIN1 = 8  # GPIO PIN 1,6,3
LDR_PIN2 = 9  # GPIO PIN 17,20,5
wpi.wiringPiSetup()

wpi.pinMode(LED_PIN1, wpi.OUTPUT)
wpi.pinMode(LED_PIN2, wpi.OUTPUT)
wpi.pinMode(LDR_PIN1, wpi.INPUT)
wpi.pinMode(LDR_PIN2, wpi.INPUT)
LDR_SCORE1 = 0
LDR_SCORE2 = 0
start_tijd = time.time()
secondes = 4

while True:
    ldr1_value = wpi.digitalRead(LDR_PIN1)
    ldr2_value = wpi.digitalRead(LDR_PIN2)
    timestamp = int(time.time())
    cursor.execute("INSERT INTO ldr_data (timestamp, ldr1, ldr2) VALUES (?,?,?)", (timestamp, ldr1_value, ldr2_value))
    conn.commit()
    time.sleep(0.125)
    # emit the LDR data in real-time
    socketio.emit('ldr_data', {'ldr1_value': ldr1_value, 'ldr2_value': ldr2_value, 'timestamp': timestamp})
    if wpi.digitalRead(LDR_PIN1) == 1:
            print(1)
    else:
        print(0)
    time.sleep(0.125)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)

       
