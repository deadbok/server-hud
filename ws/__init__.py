#!/usr/bin/python

import os
import types
import json
import tornado.websocket

from ws.log import logger

from ws import accesses
from ws import connections
from ws import remote_host
from ws import uptime
from ws import speed

from config import CONFIG

__version__ = '0.0.1'

class WebSocketServicesHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message(json.dumps(CONFIG['WS_SERVICES']))

    def on_message(self, message):
        logger.debug("Sending services message: " +
                     CONFIG['WS_SERVICES'])
        self.write_message(json.dumps(CONFIG['WS_SERVICES']))

    def on_close(self):
        logger.debug("Connection was closed...")

handlers = []
for service in CONFIG['WS_SERVICES']:
    logger.info("Adding WebSocket service: " + service)
    handlers.append((r"/ws/" + service, getattr(globals()[service], "WebSocket" + service + "Handler")))

handlers.append((r"/ws/services", WebSocketServicesHandler))
APP = tornado.web.Application(handlers=handlers, autoreload=True)
