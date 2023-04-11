import time
import mysql.connector
import odroid_wiringpi as wpi
import datetime

#break beam setup
BEAM_10 = 3

wpi.wiringPiSetup()
wpi.pinMode(BEAM_10, wpi.INPUT)

# Connect to the database
database = mysql.connector.connect(
  host="oege.ie.hva.nl",
  user="bruggev",
  password="#bnbpLjKr6L8mx",
  database="zbruggev"
)

# Create a cursor object for executing SQL queries
cursor = database.cursor()

# beam state bij variable 
beamTen_state = wpi.digitalRead(BEAM_10)
global score
score = 0
print(score)
while True:
    print(score)
    time.sleep(3)
    if beamTen_state == wpi.LOW:
        score += 10
        scoreTimestamp = datetime.datetime.now()
        sql = "INSERT INTO breakBeam (timestamp, score) VALUES (%s, %s)"
        val = (scoreTimestamp, score)
        cursor.execute(sql, val)

        database.commit()

        print(cursor.rowcount, "record inserted.")

        print('In database?')
        print(score)
        print(scoreTimestamp)
        time.sleep(3)
