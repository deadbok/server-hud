'''
:since: 01/08/2015
:author: oblivion
'''
from datetime import datetime
from socket import getfqdn
import socket

from flask import abort
from flask import jsonify
from flask import render_template
from flask import request
from flask.helpers import make_response
from flask.json import jsonify
import psutil
import requests

from app import APP
from app.log import logger


AVG_RCV_SPEED = 0
AVG_SEND_SPEED = 0
LAST_RCV_BYTES = 0
LAST_SEND_BYTES = 0
LAST_RCV_TIME = 0
LAST_SEND_TIME = 0


def cors_answer_options():
    '''
    Handles answering the first part of the CORS request.
    '''
    if 'Origin' in request.headers:
        logger.debug("CORS request from: " + request.headers['Origin'] + ".")
        if request.headers['Origin'] in APP.config['ALLOWED'] and \
        request.headers['Access-Control-Request-Method'] == 'GET' and \
        request.headers['Access-Control-Request-Headers'] == 'content-type':
            resp = make_response('')
            resp.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
            resp.headers['Access-Control-Allow-Methods'] = 'GET'
            resp.headers['Access-Control-Allow-Headers'] = 'content-type'
            return resp
    logger.debug("CORS request failed.")
    abort(401)


def add_cors_headers(json):
    '''
    Added CORS headers if necessary.
    '''
    rsp = make_response(json)

    if 'Origin' in request.headers.keys() \
    and 'content-type' in request.headers:
        logger.debug('Adding CORS headers to response.')
        rsp.headers['Access-Control-Allow-Origin'] = request.headers['Origin']

    return rsp


def index():
    '''
    Render the template for the dash board.
    '''
    logger.debug("Rendering dash board template.")
    return render_template('index.html', hostname=getfqdn())


def connections():
    '''
    Return a JSON object with number of connections on a port.
    '''
    logger.debug("Getting active connections.")

    if request.method == 'OPTIONS':
        return cors_answer_options()

    active = 0
    # Get connections on port 80
    conn = psutil.net_connections('inet')
    if APP.config['PORT'] == 'all':
        logger.debug("Counting all active connections.")
        for connection in conn:
            active += 1
    else:
        logger.debug("Counting connections on port: " +
                     APP.config['PORT'] + ".")
        for connection in conn:
            if connection.laddr[1] == int(APP.config['PORT']):
                active += 1
    # Return JSON
    logger.debug("Connections: " + str(active))
    return add_cors_headers(jsonify(connections=active))


def rcv_speed():
    '''
    Return average speed during the last 2 calls in JSON.
    '''
    global AVG_RCV_SPEED
    global LAST_RCV_BYTES
    global LAST_RCV_TIME

    logger.debug("Get average incoming speed.")

    if request.method == 'OPTIONS':
        return cors_answer_options()

    try:
        interfaces = psutil.net_io_counters(True)
        now = datetime.now()
        total_bytes_recv = interfaces[APP.config['INTERFACE']].bytes_recv

        if LAST_RCV_TIME == 0:
            LAST_RCV_BYTES = total_bytes_recv
            LAST_RCV_TIME = now
            logger.debug("First run, no average yet.")
            return jsonify(speed=0)

        time = (now - LAST_RCV_TIME).seconds
        logger.debug("Sample period: " + str(time) + " seconds.")
        rcv_bytes = total_bytes_recv - LAST_RCV_BYTES
        logger.debug("Bytes received: " + str(rcv_bytes) + " bytes.")
        speed = (rcv_bytes / time) / 1024
        logger.debug("Sampled speed: " + str(speed) + "KiB/s.")

        AVG_RCV_SPEED = (AVG_RCV_SPEED + speed) / 2
        logger.debug("Average speed: " + str(AVG_RCV_SPEED) + " KiB/s.")
        LAST_RCV_BYTES = total_bytes_recv
        LAST_RCV_TIME = now
    except ZeroDivisionError:
        logger.warning("Sampling to fast, while sampling incoming speed.")
    except KeyError:
        logger.error("Interface not found.")

    return add_cors_headers(jsonify(speed="{0:.2f}".format(AVG_RCV_SPEED)))


def send_speed():
    '''
    Return average speed during the last 2 calls in JSON.
    '''
    global AVG_SEND_SPEED
    global LAST_SEND_BYTES
    global LAST_SEND_TIME

    logger.debug("Get average outgoing speed.")

    if request.method == 'OPTIONS':
        return cors_answer_options()

    try:
        interfaces = psutil.net_io_counters(True)
        now = datetime.now()
        total_bytes_sent = interfaces[APP.config['INTERFACE']].bytes_sent

        if LAST_SEND_TIME == 0:
            LAST_SEND_BYTES = total_bytes_sent
            LAST_SEND_TIME = now
            logger.debug("First run, no average yet.")
            return jsonify(speed=0)

        time = (now - LAST_SEND_TIME).seconds
        logger.debug("Sample period: " + str(time) + " seconds.")
        sent_bytes = total_bytes_sent - LAST_SEND_BYTES
        logger.debug("Bytes sent: " + str(sent_bytes) + " bytes.")
        speed = (sent_bytes / time) / 1024
        logger.debug("Sampled speed: " + str(speed) + "KiB/s.")

        AVG_SEND_SPEED = (AVG_SEND_SPEED + speed) / 2
        logger.debug("Average speed: " + str(AVG_SEND_SPEED) + " KiB/s.")
        LAST_SEND_BYTES = total_bytes_sent
        LAST_SEND_TIME = now
    except ZeroDivisionError:
        logger.warning("Sampling to fast, while sampling outgoing speed.")
    except KeyError:
        logger.error("Interface not found.")

    return add_cors_headers(jsonify(speed="{0:.2f}".format(AVG_SEND_SPEED)))


def uptime():
    '''
    Return uptime of the server process.
    '''
    logger.debug('Getting up time for "' + APP.config['PROCESS_NAME'] + '".')

    if request.method == 'OPTIONS':
        return cors_answer_options()

    proc_time = 0

    # Find the lighttpd process and get the create time, to calculate the up
    # time.
    for process in psutil.process_iter():
        if process.name().find(APP.config['PROCESS_NAME']) != -1:
            logger.debug("Process found.")
            proc_time = (datetime.now() -
                         datetime.fromtimestamp(process.create_time()))
    logger.debug("Up time: " + str(proc_time) + ".")
    proc_time = str(proc_time).split('.')[0]

    return add_cors_headers(jsonify(uptime=proc_time))


def remote_host():
    '''
    Return name of the remote host.
    '''
    logger.debug("Getting last remote host from access log.")

    if request.method == 'OPTIONS':
        return cors_answer_options()

    # Get latest remote address from access.log.
    lines = list()
    try:
        with open(APP.config['ACCESS_LOG'], "rt") as log_file:
            # And so lets waste a lot of memory, said the programmer.
            lines = log_file.readlines()
        log_file.close()
    except PermissionError:
        logger.error("Permission denied reading log file: " +
                     APP.config['ACCESS_LOG'])
        lines.append("Permission denied reading server log file.")

    logger.debug("Log line: " + lines[-1] + ".")
    ip_addr = lines[-1].split(' ')[0]

    rhost = socket.gethostbyaddr(ip_addr)
    logger.debug("Host name from DNS: " + str(rhost) + ".")

    return add_cors_headers(jsonify(address=rhost[0]))


def accesses():
    '''
    Return number of accesses logged..
    '''
    if request.method == 'OPTIONS':
        return cors_answer_options()

    # Get latest remote address from access.log.
    lines = list()
    try:
        with open(APP.config['ACCESS_LOG'], "rt") as log_file:
            # And so lets waste a lot of memory, said the programmer.
            lines = log_file.readlines()
        log_file.close()
    except PermissionError:
        logger.error("Permission denied reading log file: " +
                     APP.config['ACCESS_LOG'])
        lines.append("Permission denied reading server log file.")

    logger.debug("Log line: " + lines[-1] + ".")

    return add_cors_headers(jsonify(accesses=len(lines)))


@APP.route('/rest/services', methods=['GET', 'OPTIONS'])
def services():
    '''
    Return the REST endpoint that are supported.
    '''
    return jsonify(services=APP.config['SERVICES'])


def build_urls():
    '''
    Build all URL using configured services from SERVICES.
    '''
    logger.debug("Building urls.")
    for service in APP.config['SERVICES']:
        if service != 'index':
            logger.debug("Adding: " + '/rest/' + service + ".")
            # Everything but index is REST.
            APP.add_url_rule('/rest/' + service, service, globals()[service],
                             methods=['GET', 'OPTIONS'])
        else:
            logger.debug("Adding: " + "/.")
            APP.add_url_rule('/', 'index', index, methods=['GET'])
