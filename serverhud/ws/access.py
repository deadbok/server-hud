'''
:since: 10/09/2016
:author: oblivion
'''
import json
import os.path
import logging

from serverhud import ws

from serverhud.ws import logger

import tornado.ioloop
from functools import partial

from watchdog.events import FileSystemEventHandler



class AccessHandler(FileSystemEventHandler):
    instances = 0

    def __init__(self, handler, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Creating WebSocket file access handler")
        super(AccessHandler, self).__init__(*args, **kwargs)
        self.handlers = [handler]
        self.accesses = 0
        self.lastline = ""
        AccessHandler.instances += 1
        self.logger.debug(str(AccessHandler.instances) + " active handlers")
        self.id = AccessHandler.instances
        self.read_access_log()

    def handle(self, data):
        self.logger.debug("(" + str(self.id) + ") Handling: " + str(data))
        for handler in self.handlers:
            self.logger.debug("(" + str(self.id) + ") Calling handler: " + str(handler))
            tornado.ioloop.IOLoop.instance().add_callback(partial(handler, data))
            #handler(data)

    def read_access_log(self):
        # Count number of lines
        self.logger.debug("(" + str(self.id) + ") Reading log file.")
        try:
            with open(ws.config.CONFIG['ACCESS_LOG']) as log_file:
                for line_number, line in enumerate(log_file, 1):
                    pass
            if (self.accesses <= line_number):
                self.accesses = line_number
            else:
                # Try compensating when logrotate empties the file.
                self.accesses += line_number
            self.lastline = line
        except FileNotFoundError:
            self.logger.exception("Could not open HTTPd access log.")
            self.accesses = -1

    def on_modified(self, event):
        filename = os.path.basename(event.src_path)
        self.logger.debug("(" + str(self.id) + ") Access: " + filename)
        if (filename == os.path.basename(ws.config.CONFIG['ACCESS_LOG'])):
            self.read_access_log()

        self.handle({"accesses": self.accesses, "lastline": self.lastline})

    def add_handler(self, handler):
        self.handlers.append(handler)

    def remove_handler(self, handler):
        if handler in self.handlers:
            self.handlers.remove(handler)
        AccessHandler.instances -= 1
        self.logger.debug(str(AccessHandler.instances) + " active handlers")
