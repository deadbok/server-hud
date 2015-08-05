'''
:since: 01/08/2015
:author: oblivion
'''
from datetime import datetime

from flask import jsonify
from flask import request
import psutil

from app import APP

from app.log import logger

AVG_RCV_SPEED = 0
AVG_SEND_SPEED = 0
LAST_RCV_BYTES = 0
LAST_SEND_BYTES = 0
LAST_RCV_TIME = 0
LAST_SEND_TIME = 0


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
    except KeyError:
            logger.error("Interface not found.")

    return jsonify(speed="{0:.2f}".format(AVG_RCV_SPEED))


@APP.route('/rest/send_speed', methods=['GET', 'OPTIONS'])
def send_speed():
    '''
    Return average speed during the last 2 calls in JSON.
    '''
    global AVG_SEND_SPEED
    global LAST_SEND_BYTES
    global LAST_SEND_TIME

    logger.debug("Get average outgoing speed.")

    if request.method == 'OPTIONS':
        logger.debug("CORS request from: " + request.headers['Origin'] + ".")

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

    return jsonify(speed="{0:.2f}".format(AVG_SEND_SPEED))
