'''
Created on 01/08/2015

@author: oblivion
'''
from datetime import datetime
from io import SEEK_END
from socket import getfqdn
import re

from flask import render_template
import psutil
import requests

from app import app


@app.route('/')
@app.route('/index')
def index():
    uptime = 0
    active = 0

    for process in psutil.process_iter():
        if (process.name().find('lighttpd') != -1):
            uptime = (datetime.now() - datetime.fromtimestamp(process.create_time()))
    uptime = str(uptime).split('.')[0]

    # Get connections on port 80
    connections = psutil.net_connections('inet')
    for connection in connections:
        if (connection.laddr[1] == 80):
            active += 1

    # Get latest remote address from access.log.
    lines = list()
    try:
        with open("/var/log/lighttpd/access.log", "rt") as log_file:
            # And so lets waste a lot of memory, said the programmer.
            lines = log_file.readlines()
        log_file.close()
    except PermissionError:
        lines.append("Permission denied reading server log file.")

    # Lighttpd has the  HTTP request host name as second field.
    entries = lines[-1].split(' ')
    # Set total requests
    accesses = len(lines)

    return render_template('index.html', title=getfqdn(), active=active, url=entries[0],
                           uptime=uptime, accesses=accesses)
