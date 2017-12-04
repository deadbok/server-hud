'''
:since: 01/08/2015
:author: oblivion
'''
from logging import handlers
import logging
from flask import Flask
from serverhud.app import views


# Init app and config
APP = Flask(__name__)
APP.config.from_envvar('SERVERHUD_CONFIG')
CONFIG = APP.config

# Start logger
if CONFIG['DEBUG']:
    APP.logger.setLevel(logging.DEBUG)
    file_log = handlers.RotatingFileHandler(CONFIG['CLIENT_LOG_FILE'],
                                            maxBytes=10000000,
                                            backupCount=5)
    file_log.setLevel(logging.DEBUG)
    file_log.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s'))
    APP.logger.addHandler(file_log)
else:
    APP.logger.setLevel(logging.CRITICAL)
    file_log = handlers.RotatingFileHandler(CONFIG['CLIENT_LOG_FILE'],
                                            maxBytes=10000000,
                                            backupCount=5)
    file_log.setLevel(logging.WARNING)
    file_log.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s'))
    APP.logger.addHandler(file_log)

# Build all URL using configured services from SERVICES.
APP.logger.debug("Building urls.")
APP.logger.debug("Adding: " + "/.")
APP.add_url_rule('/', 'index', views.index, methods=['GET'])
