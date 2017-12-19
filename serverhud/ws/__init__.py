#!/usr/bin/python

import os
import types
import json
import tornado.websocket
from urllib.parse import urlparse
from tornado.options import options

from serverhud.ws import config
from serverhud.ws.log import logger

from serverhud.ws import accesses
from serverhud.ws import connections
from serverhud.ws import remote_host
from serverhud.ws import uptime
from serverhud.ws import speed


class WebSocketServicesHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message(json.dumps(ws.config.CONFIG['WS_SERVICES']))

    def on_message(self, message):
        logger.debug("Sending services message: " +
                     config.CONFIG['WS_SERVICES'])
        self.write_message(json.dumps(config.CONFIG['WS_SERVICES']))

    def on_close(self):
        logger.debug("Connection was closed...")


def init():
    handlers = []
    for service in config.CONFIG['WS_SERVICES']:
        logger.info("Adding WebSocket service: " + service)
        handlers.append(
            (r"/ws/" + service,
             getattr(globals()[service],
                     "WebSocket" + service + "Handler"
                     )
             )
            )

    handlers.append((r"/ws/services", WebSocketServicesHandler))
    app = tornado.web.Application(handlers=handlers, autoreload=True)

    return app


def origin_allowed(origin):
    '''
    Check if an origin from a request is allowed access.
    '''
    host = urlparse(origin).netloc
    if host in config.CONFIG['ALLOWED']:
        logger.debug("Allowing: " + host)
        return(True)

    logger.debug("Denying: " + host)
    return(False)
