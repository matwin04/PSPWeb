from bottle import route, run, template, static_file
import sqlite3
import os
import  socket
from cli_color_py import green

hostname = socket.gethostbyname()
ipaddr = socket.gethostbyname(hostname)
print(green(f"RUNNING PSP CLASSIC WEB ON {hostname}"))

