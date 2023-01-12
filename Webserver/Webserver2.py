from flask import Flask, render_template
import sqlite3

app = Flask(__name__, template_folder='templates', static_folder='static')
conn = sqlite3.connect('ldr_data.db')
cursor = conn.cursor()

@app.route('/')
def index():
    # Retrieve the data from the ldr_data table
    cursor.execute("SELECT * FROM ldr_data")
    data = cursor.fetchall()

    # Render the data in the template
    return render_template('index.html', data=data)

@app.route('/status.html')
def status():
    return render_template('status.html')

@app.route('/data.html')
def data():
    return render_template('data.html')

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=5000)
