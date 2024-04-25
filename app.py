from bottle import route, run, template, static_file
import sqlite3
import os
@route('/pages/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./pages/')

@route('/')
def index():
    return template('./pages/index.html')
run(host='localhost',port=5150, debug=True, reloader=True)
print("run")