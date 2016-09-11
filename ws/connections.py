'''
:since: 10/09/2016
:author: oblivion
'''
import json
import psutil

import tornado.websocket
import tornado.ioloop

from ws.config import CONFIG
from ws.log import logger


HANDLER = None
OBSERVER = None

class WebSocketconnectionsHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        logger.debug("Creating WebSocket connections handler")
        super(WebSocketconnectionsHandler, self).__init__(*args, **kwargs)
        # No WebSocket connection yet
        self.connected = False
        # We have not counted the connections yet
        self.connections = 0
        # Update the connection count
        self.update()

    def get_connections(self):
        self.connections = 0
        # Get all connections using psutil
        conn = psutil.net_connections('inet')

        if CONFIG['PORT'][0] == 'all':
            # If we need the count for all ports we've got it.
            for connection in conn:
                self.connections += 1
        else:
            # Isolate date for the requested ports.
            for port in CONFIG['PORT']:
                for connection in conn:
                    if connection.laddr[1] == int(port):
                        self.connections += 1

        return(self.connections)

    def update(self):
        # Save the old number of connections
        old = self.connections
        self.get_connections()

        # Check if the number opf connections has changed
        if old != self.connections:
            if (self.connected):
                # Send the new data.
                if self.connected:
                    logger.debug(json.dumps({ "connections": self.get_connections() }))
                    self.write_message(json.dumps({ "connections": self.get_connections() }))

        # Keep adding the update function to the callbacks that Tornado's IOLoop
        # call the next time around.
        tornado.ioloop.IOLoop.instance().add_callback(callback=self.update)

    def open(self):
        logger.debug(json.dumps({ "connections": self.get_connections() }))
        self.write_message(json.dumps({ "connections": self.get_connections() }))
        # We have a WebSocket connection
        self.connected = True

    def on_message(self, message):
        logger.debug(json.dumps({ "connections": self.get_connections() }))
        self.write_message(json.dumps({ "connections": self.get_connections() }))

    def on_close(self):
        logger.debug("Connection closed")
        # We no longer have a WebSocket connection.
        self.connected = False
