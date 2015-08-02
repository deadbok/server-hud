'''
Created on 01/08/2015

@author: oblivion
'''
from io import SEEK_END
from socket import getfqdn
import re

from flask import render_template
import requests

from app import app


@app.route('/')
@app.route('/index')
def index():
    # Get data from the lighttpd status addon
    r = requests.get("http://" + getfqdn() + "/server-status?auto")

    pattern = re.compile('(\w+:.)(\d+)')
    entry_iter = pattern.finditer(r.text)
    for match in entry_iter:
        if (match.group(1).find("Uptime") != -1):
            uptime = int(match.group(2))
        elif (match.group(1).find("Accesses") != -1):
            accesses = int(match.group(2))
        elif (match.group(1).find("BusyServers") != -1):
            active = int(match.group(2))

    # Get latest remote address from access.log.
    lines = list()
    try:
        with open("/var/log/lighttpd/access.log", "rt") as log_file:
            # And so lets waste a lot of memory, said the programmer.
            lines = log_file.readlines()
        log_file.close()
    except PermissionError:
        lines.append("Permission denied reading server log file.")

    line = lines[-1]

    print(lines)

    return render_template('index.html', title=getfqdn(), active=active, url=line,
                           uptime=uptime, accesses=accesses)
