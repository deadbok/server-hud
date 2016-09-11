'''
:since: 10/09/2016
:author: oblivion
'''
import json
import os.path

import tornado.websocket
import tornado.ioloop

from watchdog.observers import Observer

from ws.log import logger
from ws.access import AccessHandler
from ws.config import CONFIG

HANDLER = None
OBSERVER = None


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
        self.send({ "accesses": HANDLER.accesses })

    def on_message(self, message):
        self.send({ "accesses": HANDLER.accesses })

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
