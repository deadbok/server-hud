#!/usr/bin/python
'''
:since: 10/09/2016
:author: oblivion
'''
import os
import logging
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
from tornado.options import define, options

import ws

from ws import __version__
from ws.config import init_config
from ws.log import logger, init_file_log, init_console_log, close_log


define("debug", default=False, help="Log debug information", type=bool)
define("port", default=5000, help="run on the given port", type=int)
define("config", default=os.getcwd() + "/config.py", help="Path to configuration file", type=str)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    init_config(options.config)
    # Init logging to file
    if options.debug:
        init_file_log(logging.DEBUG, ws.config.CONFIG['LOG_FILE'])
    else:
        init_file_log(logging.INFO, ws.config.CONFIG['LOG_FILE'])

    # init_file_log(logging.DEBUG)

    app = ws.init()
    logger.info("server-hud WebSocket server version " + __version__)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    logger.info("Listening on port: " + str(options.port))

    tornado.ioloop.IOLoop.instance().start()