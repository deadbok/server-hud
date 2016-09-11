'''
:since: 10/09/2016
:author: oblivion
'''
import json
import os.path

from ws.log import logger

from watchdog.events import FileSystemEventHandler

from ws.config import CONFIG

class AccessHandler(FileSystemEventHandler):
    def __init__(self, handler, *args, **kwargs):
        logger.debug("Creating WebSocket file access handler")
        super(AccessHandler, self).__init__(*args, **kwargs)
        self.handlers = [handler]
        self.accesses = 0
        self.lastline = ""
        self.read_access_log()

    def handle(self, data):
        logger.debug("Handling: " + str(data))
        for handler in self.handlers:
            logger.debug("Calling handler")
            handler(data)

    def read_access_log(self):
        # Count number of lines
        with open(CONFIG['ACCESS_LOG']) as log_file:
            for line_number, line in enumerate(log_file, 1):
                pass
        if (self.accesses <= line_number):
            self.accesses = line_number
        else:
            # Try compensating when logrotate empties the file.
            self.accesses += line_number
        self.lastline = line

    def on_modified(self, event):
        filename = os.path.basename(event.src_path)
        logger.debug("Access: " + filename)
        if (filename == os.path.basename(CONFIG['ACCESS_LOG'])):
            self.read_access_log()

        self.handle({ "accesses": self.accesses, "lastline": self.lastline})

    def add_handler(self, handler):
        self.handlers.append(handler)

    def remove_handler(self, handler):
        if handler in self.handlers:
            self.handlers.remove(handler)
