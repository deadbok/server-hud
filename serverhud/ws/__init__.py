#!/usr/bin/python

import os
import types
import json
import tornado.websocket
from urllib.parse import urlparse
from tornado.options import options

import logging
import sys

from serverhud.ws import config
from serverhud.ws.log import logger

from serverhud.ws import accesses
from serverhud.ws import connections
from serverhud.ws import remote_host
from serverhud.ws import uptime
from serverhud.ws import speed


class WebSocketServicesHandler(tornado.websocket.WebSocketHandler):
    def __init(self):
        self.logger = logging.getLogger(__name__)

    def open(self):
        self.write_message(json.dumps(ws.config.CONFIG['WS_SERVICES']))

    def on_message(self, message):
        self.logger.debug("Sending services message: " +
                          config.CONFIG['WS_SERVICES'])
        self.write_message(json.dumps(config.CONFIG['WS_SERVICES']))

    def on_close(self):
        self.logger.debug("Connection was closed...")


def init():
    handlers = []
    log = logging.getLogger(__name__)
    for service in config.CONFIG['WS_SERVICES']:
        log.info("Adding WebSocket service: " + service)
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
    log = logging.getLogger(__name__)
    host = urlparse(origin).netloc
    log.debug("Allowed:")
    for allowed in config.CONFIG['ALLOWED']:
        log.debug(" - " + allowed)
    if host in config.CONFIG['ALLOWED']:
        log.debug("Allowing: " + origin)
        return(True)

    log.debug("Denying: " + origin)
    return(False)
