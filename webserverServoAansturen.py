from flask import Flask, render_template
import odroid_wiringpi as wpi
import time

app = Flask(__name__, template_folder='.')

status = 0


def lamp():
    global status
    while status == 1:

        wpi.digitalWrite(LED_PIN, wpi.HIGH)
        time.sleep(1)
        wpi.digitalWrite(LED_PIN, wpi.LOW)
        time.sleep(1)

def lamp_uit():
    global status
    while status == 0:
        wpi.digitalWrite(LED_PIN, wpi.LOW)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/aan')
def aan():
    global status
    status = 1
    return lamp()

@app.route('/uit')
def uit():
    global status
    status = 0
    return lamp_uit()
