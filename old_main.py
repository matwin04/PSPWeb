from bottle import redirect, request, route, run, template, static_file
import sqlite3
import os
import socket

hostname = socket.gethostname()
ipaddr = socket.gethostbyname(hostname)

@route('/pages/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./pages/')

@route('/storage/<filename:path>')
def storage(filename):
    return static_file(filename,root='./storage/',download=filename)
@route('/')
def index():
    return template('./pages/index.html')


@route('/info')
def info():
    return template('./pages/index.html')

@route('/files')
def files():
    return template('./pages/files.html')

@route('/files/upload')
def upload():
    return template('./pages/new_file.html')

@route('/files/upload',method='POST')
def do_upload():
    nickname = request.forms.get('name')
    upload = request.files.get('upload')
    if upload is not None:
        name, ext = os.path.splitext(upload.filename)
        save_path = "./storage"
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        upload.save(save_path)

        conn = sqlite3.connect('content.db')
        c = conn.cursor()
        fname = name + ext()
        c.execute('INSERT INTO files (fname, name, ext) VALUES (?,?,?)', (fname,name,ext))
        conn.commit()
        conn.close()
        return redirect('/files')
    else:
        return "NO FILE UPLOADED"
run(host=ipaddr,port=5150, debug=True, reloader=True)
print("run")
