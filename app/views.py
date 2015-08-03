'''
:since: 01/08/2015
:author: oblivion
'''
from datetime import datetime
from socket import getfqdn

from flask import jsonify
from flask import render_template
import psutil

from app import APP

from app.log import logger

AVG_RCV_SPEED = 0
AVG_SEND_SPEED = 0
LAST_RCV_BYTES = 0
LAST_SEND_BYTES = 0
LAST_RCV_TIME = 0
LAST_SEND_TIME = 0


@APP.route('/', methods=['GET'])
@APP.route('/index', methods=['GET'])
def index():
    '''
    Render the template for the dash board.
    '''
    logger.debug("Rendering dash board template.")
    return render_template('index.html', hostname=getfqdn())


@APP.route('/rest/connections', methods=['GET'])
def connections():
    '''
    Return a JSON object with number of connections on a port.
    '''
    logger.debug("Getting active connections.")
    active = 0
    # Get connections on port 80
    conn = psutil.net_connections('inet')
    for connection in conn:
        if connection.laddr[1] == APP.config['PORT']:
            active += 1
    # Return JSON
    logger.debug("Connections: " + str(active))
    return jsonify(connections=active)


@APP.route('/rest/receive_speed', methods=['GET'])
def rcv_speed():
    '''
    Return average speed during the last 2 calls in JSON.
    '''
    global AVG_RCV_SPEED
    global LAST_RCV_BYTES
    global LAST_RCV_TIME

    logger.debug("Get average incoming speed.")

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

    return jsonify(speed="{0:.2f}".format(AVG_RCV_SPEED))


@APP.route('/rest/send_speed', methods=['GET'])
def send_speed():
    '''
    Return average speed during the last 2 calls in JSON.
    '''
    global AVG_SEND_SPEED
    global LAST_SEND_BYTES
    global LAST_SEND_TIME

    logger.debug("Get average outgoing speed.")

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

    return jsonify(speed="{0:.2f}".format(AVG_SEND_SPEED))


@APP.route('/rest/uptime', methods=['GET'])
def uptime():
    '''
    Return uptime of the server process.
    '''
    logger.debug('Getting up time for "' + APP.config['PROCESS_NAME'] + '".')
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

    return jsonify(uptime=proc_time)


@APP.route('/rest/remote_host', methods=['GET'])
def remote_host():
    '''
    Return name of the remote host.
    '''
    logger.debug("Getting last remote host from access log.")
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

    return jsonify(address=lines[-1].split(' ')[0])


@APP.route('/rest/accesses', methods=['GET'])
def accesses():
    '''
    Return number of accesses logged..
    '''
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

    return jsonify(accesses=len(lines))
