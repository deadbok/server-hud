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


HANDLER = None
OBSERVER = None


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
        if not self.observer:
            HANDLER = AccessHandler(handler=getattr(self, 'send'))
            OBSERVER = Observer()
            log_dir, _ = os.path.split(CONFIG['ACCESS_LOG'])
            logger.info("Watching file: " + log_dir)
            OBSERVER.schedule(HANDLER, log_dir, recursive=True)
            try:
                OBSERVER.start()
            except OSError:
                logger.error('Cannot start observer')
                self.close()
                return
        self.observer = True
        self.send({ "lastline": HANDLER.lastline})

    def on_message(self, message):
        self.send({ "lastline": HANDLER.lastline})

    def on_close(self):
        global HANDLER, OBSERVER
        logger.debug("Connection closed")
        self.connected = False
        if self.observer:
            HANDLER.remove_handler(getattr(self, 'send'))
            OBSERVER.stop()
            OBSERVER = None
            HANDLER = None
            self.observer = False
