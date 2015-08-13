'''
:since: 01/08/2015
:author: oblivion
'''
from logging import handlers
import logging
from flask import Flask
from app import views


# Init app and config
APP = Flask(__name__)
APP.config.from_object('config')
CONFIG = APP.config

# Start logger
if APP.config['DEBUG']:
    APP.logger.setLevel(logging.DEBUG)
    file_log = handlers.RotatingFileHandler("server-hud.log",
                                       maxBytes=10000000,
                                       backupCount=5)
    file_log.setLevel(logging.DEBUG)
    file_log.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s'))
    APP.logger.addHandler(file_log)
else:
    APP.logger.setLevel(logging.CRITICAL)
    file_log = handlers.RotatingFileHandler("server-hud.log",
                                       maxBytes=10000000,
                                       backupCount=5)
    file_log.setLevel(logging.WARNING)
    file_log.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s'))
    APP.logger.addHandler(file_log)

# Build all URL using configured services from SERVICES.
APP.logger.debug("Building urls.")
for service in CONFIG['SERVICES']:
    if service != 'index':
        APP.logger.debug("Adding: " + '/rest/' + service + ".")
        # Everything but index is REST.
        APP.add_url_rule('/rest/' + service, service, getattr(views, service),
                         methods=['GET', 'OPTIONS'])
    else:
        APP.logger.debug("Adding: " + "/.")
        APP.add_url_rule('/', 'index', views.index, methods=['GET'])
APP.add_url_rule('/rest/services', 'services', getattr(views, 'services'),
                 methods=['GET', 'OPTIONS'])
