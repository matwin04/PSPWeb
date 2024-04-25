from bottle import route, run, template, static_file
import sqlite3
import os
def fetch_data():
    conn = sqlite3.connect('net.db')
    c = conn.cursor()
    c.execute("SELECT * FROM devices")
    data = c.fetchall()
    c.close()
    return data
def determine_status():
    data = fetch_data()
    online_devices = sum(1 for row in data if row[3] == 'online')
    total_devices = len(data)
    return online_devices, total_devices

@route('/pages/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./pages/')

@route('/')
def index():
    return template('./pages/index.html')
run(host='localhost',port=5150, debug=True, reloader=True)
print("run")