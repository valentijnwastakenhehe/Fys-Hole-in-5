from flask import Flask, render_template
<<<<<<< HEAD:Webserver/Webserver2.py
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
=======
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    # Connect to the database
    conn = mysql.connector.connect(
        host="oege.ie.hva.nl",
        user="bruggev",
        password="#bnbpLjKr6L8mx",
        database="zbruggev"
    )
    c = conn.cursor()
>>>>>>> 3e445a187852772b7d84b8d3c8d4625b46cc0448:Webserver/Webserver.py

    # Execute a SELECT statement to retrieve the data
    c.execute('SELECT * FROM mytable')
    data = c.fetchall()

    # Close the connection
    conn.close()

    # Render the template and pass in the data
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=90)
