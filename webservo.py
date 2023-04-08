from flask import Flask, render_template
import odroid_wiringpi as wpi
import time

app = Flask(__name__, template_folder='templateservo')


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


if __name__ == '__main__':

   SERVO_PIN = 1


   wpi.wiringPiSetup()
   wpi.pinMode(SERVO_PIN, wpi.PWM_OUTPUT)

   app.run(host="0.0.0.0", port=4009)

