import webbrowser
import mysql.connector

database = mysql.connector.connect(
  host="oege.ie.hva.nl",
  user="bruggev",
  password="#bnbpLjKr6L8mx",
  database="zbruggev"
)

# Create a cursor object for executing SQL queries
cursor = database.cursor()

breakBeam = "SELECT timestamp, score FROM breakBeam"

cursor.execute(breakBeam)

result = cursor.fetchall()

p = []

tbl = "<tr><th>Timestamp</th><th>Score</th></tr>"

p.append(tbl)

for row in result:
    a = "<tr><td>%s</td>"%row[0]
    p.append(a)
    b = "<td>%s</td></tr>"%row[1]
    p.append(b)


contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta content="text/html; charset=ISO-8859-1"
http-equiv="content-type">
<title>Break beam data</title>
<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
</style>
</head>
<body>
<table>
  <caption> Score and timestamp </caption>
%s
</table>
</body>
</html>
'''%(p)

filename = 'templates/breakBeam.html'

def main(contents, filename):
    output = open(filename,"w")
    output.write(contents)
    output.close()

main(contents, filename)    
webbrowser.open(filename)
