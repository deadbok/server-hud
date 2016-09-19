'''
Get current transfer rate on an interface.

:since: 10/09/2016
:author: oblivion
'''
import json
import psutil

import tornado.websocket
import tornado.ioloop
from tornado.ioloop import PeriodicCallback

from ws.config import CONFIG
from ws.log import logger


class WebSocketspeedHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        logger.debug("Creating WebSocket speed handler")
        super(WebSocketconnectionsHandler, self).__init__(*args, **kwargs)
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
        self.last_times = (0, 0)
        self.last_bytes = (0, 0)
        self.avg_speeds = (0, 0)

    def update(self):
        if self.connected:
            logger.debug("Get average incoming speed.")

            try:
                interfaces = psutil.net_io_counters(True)
                now = datetime.now()
                total_bytes_recv = interfaces[CONFIG['INTERFACE']].bytes_recv
                total_bytes_sent = interfaces[CONFIG['INTERFACE']].bytes_sent

                time = (now - self.last_rcv_time).seconds
                logger.debug("Sample period: " + str(time) + " seconds.")

                if self.last_times[0] == 0:
                    self.last_bytes[0] = total_bytes_recv
                    self.last_times[0] = now
                    logger.debug("First receive run, no average yet.")
                else:
                    rcv_bytes = total_bytes_recv - self.last_bytes[0]
                    logger.debug("Bytes received: " + str(rcv_bytes) + " bytes.")
                    speed = (rcv_bytes / time) / 1024
                    logger.debug("Sampled receive speed: " + str(speed) + "KiB/s.")

                    self.avg_speeds[0] = (self.avg_speeds[0] + speed) / 2
                    logger.debug("Average receive  speed: " + str(self.avg_speeds[0]) +
                                 " KiB/s.")
                    self.last_bytes[0] = total_bytes_recv
                    self.last_times[0] = now

                if self.last_times[1] == 0:
                    self.last_bytes[1] = total_bytes_recv
                    self.last_rcv_time[1] = now
                    logger.debug("First receive run, no average yet.")
                else:
                    rcv_bytes = total_bytes_recv - self.last_bytes[1]
                    logger.debug("Bytes received: " + str(rcv_bytes) + " bytes.")
                    speed = (rcv_bytes / time) / 1024
                    logger.debug("Sampled receive speed: " + str(speed) + "KiB/s.")

                    self.avg_speeds[1] = (self.avg_speeds[1] + speed) / 2
                    logger.debug("Average receive  speed: " + str(self.avg_speeds[1]) +
                                 " KiB/s.")
                    self.last_bytes[1] = total_bytes_recv
                    self.last_times[1] = now

            except ZeroDivisionError:
                current_app.logger.warning("Sampling to fast, while sampling incoming speed.")
            except KeyError:
                current_app.logger.error("Interface not found.")

            logger.debug(json.dumps({ "receive": self.avg_speeds[0],
                                     "send": self.avg_speeds[1]}))
            self.write_message(json.dumps({ "receive": self.avg_speeds[0],
                                               "send": self.avg_speeds[1]}))

    def open(self):
        logger.debug(json.dumps({ "connections": self.get_connections() }))
        self.write_message(json.dumps({ "connections": self.get_connections() }))
        # We have a WebSocket connection
        self.connected = True
        self.periodic_callback.start()

    def on_message(self, message):
            logger.debug(json.dumps({ "receive": self.avg_speeds[0],
                                     "send": self.avg_speeds[1]}))
            self.write_message(json.dumps({ "receive": self.avg_speeds[0],
                                               "send": self.avg_speeds[1]}))

    def on_close(self):
        logger.debug("Connection closed")
        # We no longer have a WebSocket connection.
        self.connected = False
        self.periodic_callback.stop()
