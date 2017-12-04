'''
:since: 10/09/2016
:author: oblivion
'''
import json
import os.path

import tornado.websocket
import tornado.ioloop

from watchdog.observers import Observer

from serverhud.ws.log import logger
from serverhud.ws.access import AccessHandler
from serverhud import ws

HANDLER = {}
OBSERVER = {}


class WebSocketaccessesHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        logger.debug("Creating WebSocket accesses handler")
        super(WebSocketaccessesHandler, self).__init__(*args, **kwargs)
        self.connected = False
        self.observer = False

    def send(self, data):
        logger.debug("Sending: " +
                     json.dumps({ "accesses": data['accesses'] }))
        self.write_message(json.dumps({ "accesses": data['accesses'] }))

    def open(self):
        global HANDLER, OBSERVER

        self.path, _ = os.path.split(ws.config.CONFIG['ACCESS_LOG'])
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
        self.send({ "accesses": HANDLER[self.path].accesses })

    def on_message(self, message):
        global HANDLER

        self.send({ "accesses": HANDLER[self.path].accesses })

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

    def check_origin(self, origin):
        return True
