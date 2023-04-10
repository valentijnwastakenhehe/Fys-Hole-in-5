import time
import mysql.connector
import odroid_wiringpi as wpi

#break beam setup
BEAM_10 = 3

wpi.wiringPiSetup()
wpi.pinMode(BEAM_10, wpi.INPUT)

# Connect to the database
db = mysql.connector.connect(
  host="oege.ie.hva.nl/",
  user="bruggev",
  password="#bnbpLjKr6L8mx",
  database="zbruggev"
)

# Create a cursor object for executing SQL queries
cursor = db.cursor()

# beam state bij variable 
beamTen_state = wpi.digitalRead(BEAM_10)

if beamTen_state == wpi.LOW:
    timestamp = int(time.time())

    sql = "INSERT INTO breakBeam (score, timestamp) VALUES (%s, %s)"
    values = (beamTen_state, timestamp)
    cursor.execute(sql, values)
    database.commit()

    # Wait for 5 seconds before reading the sensor data again
    time.sleep(5)
