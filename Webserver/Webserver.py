from flask import Flask, render_template
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

    # Execute a SELECT statement to retrieve the data
    c.execute('SELECT * FROM mytable')
    data = c.fetchall()

    # Close the connection
    conn.close()

    # Render the template and pass in the data
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
