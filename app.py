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
    online_devices, total_devices = determine_status()
    if online_devices == total_devices:
        overall_stat_text = "All Devices Online"
        
    data = fetch_data()
    output = template('./pages/index.html',
                    data=data
                    )
    return output
run(host='localhost',port=5150, debug=True, reloader=True)
print("run")