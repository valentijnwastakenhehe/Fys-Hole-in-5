import time
import mysql.connector
import odroid_wiringpi as wpi

#break beam setup
BEAM_10 = 3

wpi.wiringPiSetup()
wpi.pinMode(BEAM_10, wpi.INPUT)

# Connect to the database
db = mysql.connector.connect(
  host="http://oege.ie.hva.nl/",
  user="bruggev",
  password="#bnbpLjKr6L8mx",
  database="zbruggev"
)

# Create a cursor object for executing SQL queries
cursor = db.cursor()

# beam state bij variable 
beamTen_state = wpi.digitalRead(BEAM_10)

# Continuously read temperature data and write it to the database
if beamTen_state == wpi.LOW:
    timestamp = int(time.time())

    # Insert the temperature and timestamp into the database
    sql = "INSERT INTO temperature_data (temperature, timestamp) VALUES (%s, %s)"
    values = (beamTen_state, timestamp)
    cursor.execute(sql, values)
    db.commit()

    # Wait for 5 seconds before reading the sensor data again
    time.sleep(5)
