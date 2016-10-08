#!/usr/bin/python

import os
import types
import json
import tornado.websocket
from tornado.options import options

import ws
from ws.log import logger

from ws import accesses
from ws import connections
from ws import remote_host
from ws import uptime
from ws import speed

__version__ = '0.0.2'

class WebSocketServicesHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message(json.dumps(ws.config.CONFIG['WS_SERVICES']))

    def on_message(self, message):
        logger.debug("Sending services message: " +
                     ws.config.CONFIG['WS_SERVICES'])
        self.write_message(json.dumps(ws.config.CONFIG['WS_SERVICES']))

    def on_close(self):
        logger.debug("Connection was closed...")

def init():
    handlers = []
    for service in ws.config.CONFIG['WS_SERVICES']:
        logger.info("Adding WebSocket service: " + service)
        handlers.append((r"/ws/" + service, getattr(globals()[service], "WebSocket" + service + "Handler")))

    handlers.append((r"/ws/services", WebSocketServicesHandler))
    app = tornado.web.Application(handlers=handlers, autoreload=True)

    return app
