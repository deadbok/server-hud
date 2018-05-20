'''
:since: 11/09/2016
:author: oblivion
'''
import json
import socket
import os.path
import logging
import datetime
import tornado.websocket
from tornado.ioloop import PeriodicCallback

from serverhud.ws import logger
from serverhud import ws


class WebSocketremote_hostHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Creating WebSocket remote_host handler")
        super(WebSocketremote_hostHandler, self).__init__(*args, **kwargs)
        self.mod_time = 0
        self.ip_addr = "none"
        self.connected = False
        self.update()
        # Setup periodic callback via Tornado
        self.periodic_callback = PeriodicCallback(getattr(self, 'update'),
                                                  1000)

    def send(self):
        if self.connected:
            self.logger.debug("Sending: " +
                            json.dumps({"remote_host": self.ip_addr}))
            self.write_message(json.dumps({"remote_host": self.ip_addr}))

    def open(self):
        self.logger.debug("Connection opened")
        self.connected = True
        self.update()
        self.periodic_callback.start()
        self.send()

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
            # Count number of lines
            self.logger.debug("Reading log file: " +
                              ws.config.CONFIG['ACCESS_LOG'])
            try:
                with open(ws.config.CONFIG['ACCESS_LOG']) as log_file:
                    lines = log_file.readlines()
                lastline = lines[-1]
                self.mod_time = new_time
                if lastline == "":
                    self.logger.info("No host found in access log.")
                    self.write_message(json.dumps({"remote_host": "none"}))
                else:
                    self.ip_addr = lastline.split(' ')[0]

                rhost = list()
                try:
                    rhost = socket.gethostbyaddr(self.ip_addr)
                except (socket.herror, socket.gaierror):
                    self.logger.debug("DNS bugged out, sending IP: " +
                                      self.ip_addr + ".")
                    rhost.append("")

                if rhost[0] != "":
                    self.ip_addr += "\n(" + rhost[0] + ")"
                    self.send()
            except FileNotFoundError:
                self.logger.exception("Could not open HTTPd access log.")
