'''
:since: 11/09/2016
:author: oblivion
'''
import json
import socket
import os.path

import tornado.websocket
import tornado.ioloop

from watchdog.observers import Observer

from ws.log import logger
from ws.access import AccessHandler
from ws.config import CONFIG


HANDLER = {}
OBSERVER = {}


class WebSocketremote_hostHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        logger.debug("Creating WebSocket remote_host handler")
        super(WebSocketremote_hostHandler, self).__init__(*args, **kwargs)
        self.connected = False
        self.observer = False
        self.ip_addr = "0.0.0.0"

    def send(self, data):
        self.ip_addr = data['lastline'].split(' ')[0]

        rhost = list()
        try:
            rhost = socket.gethostbyaddr(self.ip_addr)
        except (socket.herror, socket.gaierror):
            logger.debug("DNS bugged out, sending IP: " + self.ip_addr + ".")
            rhost.append("")

        if rhost[0] != "":
            self.ip_addr += " (" + rhost[0] + ")"
        logger.debug("Sending: " +
                     json.dumps({ "remote_host": self.ip_addr }))
        self.write_message(json.dumps({ "remote_host": self.ip_addr }))

    def open(self):
        global HANDLER, OBSERVER
        
        self.path, _ = os.path.split(CONFIG['ACCESS_LOG'])
        if self.path not in HANDLER:
            HANDLER[self.path] = AccessHandler(handler=getattr(self, 'send'))
            OBSERVER[self.path] = Observer()
            logger.info("Watching: " + self.path)
            OBSERVER[self.path].schedule(HANDLER[self.path], self.path, recursive=True)
            try:
                OBSERVER[self.path].start()
            except OSError:
                logger.error('Cannot start observer')
                self.close()
                return
        self.observer = True
        self.send({ "lastline": HANDLER[self.path].lastline})

    def on_message(self, message):
        global HANDLER
        
        self.send({ "lastline": HANDLER[self.path].lastline})

    def on_close(self):
        global HANDLER, OBSERVER
        
        logger.debug("Connection closed")
        self.connected = False
        if self.observer:
            logger.debug("Stop watching:" + self.path)
            HANDLER[self.path].remove_handler(getattr(self, 'send'))

            if len(HANDLER[self.path].handlers):
                OBSERVER[self.path].stop()
                del OBSERVER[self.path]
                del HANDLER[self.path]
                self.observer = False
