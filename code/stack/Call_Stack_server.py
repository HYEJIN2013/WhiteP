#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    from utils import cheese  # utils.cheese() draws the call stack graph
    cheese()
    return 'Yet another hello!'

if __name__ == '__main__':
    app.run()
