#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import Tkinter as tk
from serial import Serial
from minirobots import Turtle
from flask import Flask, request, render_template

try:
    serial = Serial('/dev/rfcomm0', 57600)
    time.sleep(1)
except OSError:
    print "Can't connect to serial device on", args.port
    sys.exit(1)

turtle = Turtle(serial)
turtle.pen_down()

app = Flask(__name__)

commands = ['forward', 'backward', 'left', 'right']

@app.route('/')
def index():
    if len(request.args.keys()) == 1 and request.args.keys()[0] in commands:
        command = request.args.keys()[0]
        value   = int(request.args.get(command))
        getattr(turtle, command)(value)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
