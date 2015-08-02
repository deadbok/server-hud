'''
Created on 01/08/2015

@author: oblivion
'''
from datetime import datetime
from socket import getfqdn

from flask import jsonify
from flask import render_template
import psutil

from app import app


@app.route('/')
@app.route('/index')
def index():
    uptime = 0

# Find the lighttpd process and get the create time, to calculate the up time.
    for process in psutil.process_iter():
        if (process.name().find('lighttpd') != -1):
            uptime = (datetime.now() -
                      datetime.fromtimestamp(process.create_time()))
    uptime = str(uptime).split('.')[0]

# Get latest remote address from access.log.
    lines = list()
    try:
        with open("/var/log/lighttpd/access.log", "rt") as log_file:
# And so lets waste a lot of memory, said the programmer.
            lines = log_file.readlines()
        log_file.close()
    except PermissionError:
        lines.append("Permission denied reading server log file.")

    remote = lines[-1].split(' ')[0]
# Set total requests
    accesses = len(lines)

    return render_template('index.html', title=getfqdn(),
                           url=remote, uptime=uptime, accesses=accesses)

@app.route('/rest/connections')
def connections():
    active = 0
# Get connections on port 80
    conn = psutil.net_connections('inet')
    for connection in conn:
        if (connection.laddr[1] == 80):
            active += 1
#Return JSON
    return jsonify(connections=active)
