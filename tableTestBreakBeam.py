import mysql.connector
import webbrowser

def connect_to_database():
    database = mysql.connector.connect(
        host="oege.ie.hva.nl",
        user="bruggev",
        password="#bnbpLjKr6L8mx",
        database="zbruggev"
    )
    return database

def get_break_beam_data(cursor):
    break_beam_query = """SELECT timestamp, score FROM breakBeam"""
    cursor.execute(break_beam_query)
    return cursor.fetchall()

def generate_html_table(result):
    p = []
    tbl = "<tr><th>Timestamp</th><th>Score</th></tr>"
    p.append(tbl)
    for row in result:
        a = "<tr><td>%s</td>"%row[0]
        p.append(a)
        b = "<td>%s</td></tr>"%row[1]
        p.append(b)
    return ''.join(p)

def write_to_file(contents, filename):
    with open(filename, 'w') as f:
        f.write(contents)

def breakBeamTable():
    database = connect_to_database()
    cursor = database.cursor()
    print('connected to database')
    result = get_break_beam_data(cursor)
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
    ''' % generate_html_table(result)
    filename = 'templates/breakBeam.html'
    write_to_file(contents, filename)
    cursor.close()
    database.close()
    print("MySQL connection is closed.")

if __name__ == '__main__':
    breakBeamTable()
