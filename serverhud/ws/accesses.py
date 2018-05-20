'''
:since: 10/09/2016
:author: oblivion
'''
import json
import os.path
import logging
import tornado.websocket
from tornado.ioloop import PeriodicCallback

from serverhud.ws import logger
from serverhud import ws

class WebSocketaccessesHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Creating WebSocket accesses handler")
        super(WebSocketaccessesHandler, self).__init__(*args, **kwargs)
        self.connected = False
        self.accesses = 0
        self.mod_time = 0
        self.update()
        # Setup periodic callback via Tornado
        self.periodic_callback = PeriodicCallback(getattr(self, 'update'),
                                                  1000)

    def send(self):
        if self.connected:
            self.logger.debug("Sending: " +
                            json.dumps({"accesses": self.accesses}))
            self.write_message(json.dumps({"accesses": self.accesses}))

    def open(self):
        self.logger.debug("Connection opened")
        self.connected = True
        self.update()
        self.send()
        self.periodic_callback.start()

    def on_message(self, message):
        self.logger.debug("Message received")
        self.send()

    def on_close(self):
        self.logger.debug("Connection closed")
        self.connected = False

    def check_origin(self, origin):
        return ws.origin_allowed(origin)

    def update(self):
            new_time = os.path.getmtime(ws.config.CONFIG['ACCESS_LOG'])
            if self.mod_time < new_time:        
                self.mod_time = new_time
                # Count number of lines
                self.logger.debug("Reading log file: " +
                                ws.config.CONFIG['ACCESS_LOG'])
                try:
                    with open(ws.config.CONFIG['ACCESS_LOG']) as log_file:
                        lines = log_file.readlines()

                    if (self.accesses <= len(lines)):
                        self.accesses = len(lines)
                    else:
                        # Try compensating when logrotate empties the file.
                        self.accesses += len(lines)
                    self.send()
                except FileNotFoundError:
                    self.logger.exception("Could not open HTTPd access log.")
                    self.accesses = -1
