'''
:since: 10/09/2016
:author: oblivion
'''
import json
import psutil
from datetime import datetime

import tornado.websocket
from tornado.ioloop import PeriodicCallback

from ws.log import logger
import ws

HANDLER = None
OBSERVER = None

class WebSocketuptimeHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        print("Creating WebSocket uptime handler")
        super(WebSocketuptimeHandler, self).__init__(*args, **kwargs)
        # No WebSocket connection yet
        self.connected = False
        # We have not counted the connections yet
        self.uptime = "00:00:00.0"
        # Setup periodic callback via Tornado
        self.periodic_callback = PeriodicCallback(getattr(self, 'send'), 1000)
        # Update the uptime
        self.update()

    def update(self):
        logger.debug("Getting uptime")
        proc_time = 0

        # Find the lighttpd process and get the create time, to calculate the up
        # time.
        for process in psutil.process_iter():
            if process.name().find(ws.config.CONFIG['PROCESS_NAME']) != -1:
                logger.debug("Process found.")
                proc_time = (datetime.now() -
                             datetime.fromtimestamp(process.create_time()))
        logger.debug("Up time: " + str(proc_time) + ".")
        self.uptime = str(proc_time).split('.')[0]

    def send(self):
        self.update()
        logger.debug(json.dumps({ "uptime": self.uptime }))
        self.write_message(json.dumps({ "uptime": self.uptime }))

    def open(self):
        # We have a WebSocket connection
        self.connected = True
        self.send()
        self.periodic_callback.start()

    def on_message(self, message):
        self.send()

    def on_close(self):
        logger.debug("Connection closed")
        self.periodic_callback.stop()
        # We no longer have a WebSocket connection.
        self.connected = False
