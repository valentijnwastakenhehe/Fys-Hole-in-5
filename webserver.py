import sqlite3
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet
from datetime import datetime


app = Flask(__name__)
socketio = SocketIO(app)

eventlet.monkey_patch()

# Connect to the database
conn = sqlite3.connect('ldr_data.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/')
def index():
    # Retrieve the data from the ldr_data table
    cursor.execute("SELECT * FROM ldr_data")
    data = cursor.fetchall()

    data = [[datetime.fromtimestamp(row[0]),row[1],row[2]] for row in data]
    # Render the data in the template
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=False)
