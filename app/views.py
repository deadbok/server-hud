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

avg_rcv_speed = 0
avgSendSpeed = 0
lastRcvBytes = 0
lastSendBytes = 0
lastRcvTime = 0
lastSendTime = 0

@app.route('/')
@app.route('/index')
def index():
    uptime = 0

# Find the lighttpd process and get the create time, to calculate the up time.
    for process in psutil.process_iter():
        if (process.name().find(app.config['PROCESS_NAME']) != -1):
            uptime = (datetime.now() -
                      datetime.fromtimestamp(process.create_time()))
    uptime = str(uptime).split('.')[0]

# Get latest remote address from access.log.
    lines = list()
    try:
        with open(app.config['ACCESS_LOG'], "rt") as log_file:
# And so lets waste a lot of memory, said the programmer.
            lines = log_file.readlines()
        log_file.close()
    except PermissionError:
        lines.append("Permission denied reading server log file.")

    remote = lines[-1].split(' ')[0]
# Set total requests
    accesses = len(lines)

    return render_template('index.html', hostname=getfqdn(),
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


@app.route('/rest/recieve_speed')
def rcv_speed():
    global avg_rcv_speed
    global lastRcvBytes
    global lastRcvTime

    interfaces = psutil.net_io_counters(True)
    now = datetime.now()
    s = interfaces[app.config['INTERFACE']].bytes_recv

    if lastRcvTime == 0:
        lastRcvBytes = s
        lastRcvTime = now
        return jsonify(speed=0)

    time = (now - lastRcvTime).seconds
    rcv_bytes = s - lastRcvBytes
    speed = (rcv_bytes / time) / 1024

    avg_rcv_speed = (avg_rcv_speed + speed) / 2
    lastRcvBytes = s

    return jsonify(speed="{0:.2f}".format(avg_rcv_speed))

@app.route('/rest/send_speed')
def send_speed():
    global avgSendSpeed
    global lastSendBytes
    global lastSendTime

    interfaces = psutil.net_io_counters(True)
    now = datetime.now()
    s = interfaces[app.config['INTERFACE']].bytes_sent

    if lastSendTime == 0:
        lastSendBytes = s
        lastSendTime = now
        return jsonify(speed=0)

    time = (now - lastSendTime).seconds
    send_bytes = s - lastSendBytes
    speed = (send_bytes / time) / 1024

    avgSendSpeed = (avgSendSpeed + speed) / 2
    lastSendBytes = s

    return jsonify(speed="{0:.2f}".format(avgSendSpeed))
