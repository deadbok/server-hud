#!/usr/bin/python
'''
:since: 10/09/2016
:author: oblivion
'''
import logging
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from ws import __version__
from ws import APP
from ws.config import CONFIG
from ws.log import logger, init_file_log, init_console_log, close_log


define("debug", default=False, help="Log debug information", type=bool)
define("port", default=5000, help="run on the given port", type=int)


if __name__ == "__main__":
    # Init logging to file
    if options.debug:
        init_file_log(logging.DEBUG)
    else:
        init_file_log(logging.INFO)
    
    init_file_log(logging.DEBUG)

    logger.info("server-hud WebSocket server version " + __version__)
    http_server = tornado.httpserver.HTTPServer(APP)
    http_server.listen(options.port)
    logger.info("Listening on port: " + str(options.port))

    tornado.ioloop.IOLoop.instance().start()
