'''
Get current transfer rate on an interface.

:since: 10/09/2016
:author: oblivion
'''
import json
import psutil

from datetime import datetime

import tornado.websocket
import tornado.ioloop
from tornado.ioloop import PeriodicCallback

from ws.config import CONFIG
from ws.log import logger


class WebSocketspeedHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        logger.debug("Creating WebSocket speed handler")
        super(WebSocketspeedHandler, self).__init__(*args, **kwargs)
        # No WebSocket connection yet
        self.connected = False
        # We have not measured yet
        self.rcv_speed = 0
        self.send_speed = 0
        # Update the connection count
        self.update()
        # Setup periodic callback via Tornado
        self.periodic_callback = PeriodicCallback(getattr(self, 'update'),
                                                  2000)
        # Setup variables for calculating the speed
        self.last_times = {"rcv": 0, "send": 0}
        self.last_bytes = {"rcv": 0, "send": 0}
        self.avg_speeds = {"rcv": 0, "send": 0}

    def update(self):
        if self.connected:
            logger.debug("Get average incoming speed for: " +
                         CONFIG['INTERFACE'])

            try:
                interfaces = psutil.net_io_counters(True)
                print(interfaces)
                now = datetime.now()
                total_bytes_recv = interfaces[CONFIG['INTERFACE'].strip()].bytes_recv
                total_bytes_sent = interfaces[CONFIG['INTERFACE']].bytes_sent
            except KeyError:
                logger.error("Interface not found.")

            try:
                if not ((self.last_times['rcv'] == 0) and
                        (self.last_times['send'] == 0)):
                    time = ((now - self.last_times['rcv']).seconds,
                            (now - self.last_times['send']).seconds)
                else:
                    time = (now, now)

                logger.debug("Receive sample period: " + str(time[0]) +
                             " seconds.")
                logger.debug("Send sample period: " + str(time[1]) +
                             " seconds.")

                if self.last_times['rcv'] == 0:
                    self.last_bytes['rcv'] = total_bytes_recv
                    self.last_times['rcv'] = now
                    logger.debug("First receive run, no average yet.")
                else:
                    rcv_bytes = total_bytes_recv - self.last_bytes['rcv']
                    logger.debug("Bytes received: " + str(rcv_bytes) +
                                 " bytes.")
                    speed = (rcv_bytes / time[0]) / 1024
                    logger.debug("Sampled receive speed: " + str(speed) +
                                 "KiB/s.")

                    self.avg_speeds['rcv'] = (self.avg_speeds['rcv'] +
                                              speed) / 2
                    logger.debug("Average receive speed: " +
                                 str(self.avg_speeds['rcv']) +
                                 " KiB/s.")
                    self.last_bytes['rcv'] = total_bytes_recv
                    self.last_times['rcv'] = now

                if self.last_times['send'] == 0:
                    self.last_bytes['send'] = total_bytes_sent
                    self.last_times['send'] = now
                    logger.debug("First send run, no average yet.")
                else:
                    sent_bytes = total_bytes_sent - self.last_bytes['send']
                    logger.debug("Bytes sent: " + str(sent_bytes) + " bytes.")
                    speed = (sent_bytes / time[1]) / 1024
                    logger.debug("Sampled send speed: " + str(speed) + "KiB/s.")

                    self.avg_speeds['send'] = (self.avg_speeds['send'] + speed) / 2
                    logger.debug("Average send speed: " + str(self.avg_speeds['send']) +
                                 " KiB/s.")
                    self.last_bytes['send'] = total_bytes_sent
                    self.last_times['send'] = now

            except ZeroDivisionError:
                logger.warning("Sampling to fast, while sampling incoming speed.")

            logger.debug(json.dumps({ "receive": str(self.avg_speeds['rcv']) +
                                     " KiB/s.",
                                     "send": str(self.avg_speeds['send']) +
                                     " KiB/s."}))
            self.write_message(json.dumps({ "receive": str(self.avg_speeds['rcv']) +
                                           " KiB/s.",
                                           "send": str(self.avg_speeds['send']) +
                                           " KiB/s."}))

    def open(self):
        logger.debug(json.dumps({ "receive": str(self.avg_speeds['rcv']) +
                                 " KiB/s.",
                                 "send": str(self.avg_speeds['send']) +
                                 " KiB/s."}))
        self.write_message(json.dumps({ "receive": str(self.avg_speeds['rcv']) +
                                       " KiB/s.",
                                       "send": str(self.avg_speeds['send']) +
                                       " KiB/s."}))
        # We have a WebSocket connection
        self.connected = True
        self.periodic_callback.start()

    def on_message(self, message):
        logger.debug(json.dumps({ "receive": str(self.avg_speeds['rcv']) +
                                 " KiB/s.",
                                 "send": str(self.avg_speeds['send']) +
                                 " KiB/s."}))
        self.write_message(json.dumps({ "receive": str(self.avg_speeds['rcv']) +
                                       " KiB/s.",
                                       "send": str(self.avg_speeds['send']) +
                                       " KiB/s."}))

    def on_close(self):
        logger.debug("Connection closed")
        # We no longer have a WebSocket connection.
        self.connected = False
        self.periodic_callback.stop()
