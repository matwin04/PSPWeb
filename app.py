from bottle import route, run, template, static_file
import sqlite3
import os
import socket

hostname = socket.gethostname()
ipaddr = socket.gethostbyname(hostname)

@route('/pages/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./pages/')

@route('/')
def index():
    return template('./pages/index.html')

@route('/classictube')
def info():
    return template('./pages/classic_tube/index.html')
run(host=ipaddr,port=5150, debug=True, reloader=True)
print("run")
