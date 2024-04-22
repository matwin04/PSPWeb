from bottle import route, run, template
import sqlite3
import os

def fetch_data():
    conn = sqlite3.connect('net.db')
    c = conn.cursor()
    c.execute("SELECT * FROM devices")
    data = c.fetchall()
    c.close()
    return data

@route('/')
def index():
    data = fetch_data()
    output = template('./pages/index.html',
                    data=data
                    )
    return output
run(host='localhost',port=5150, debug=True, reloader=True)
print("run")