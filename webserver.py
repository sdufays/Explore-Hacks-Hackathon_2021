from flask import Flask, escape, request, render_template, Response
import time
import socket
import io
import logging
import os
import threading
from threading import Condition


app=Flask(__name__)


#HOME HTML TEMPLATE
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('Diversity.html')

app.run(host= '0.0.0.0', port=8080, debug=True, threaded=True)
