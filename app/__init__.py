'''
:since: 01/08/2015
:author: oblivion
'''
import logging

from flask import Flask
from app import views
from app.log import logger, init_file_log, init_console_log

# Init app and config
APP = Flask(__name__)
APP.config.from_object('config')
CONFIG = APP.config

# Start logger
if APP.config['DEBUG']:
    init_console_log(logging.DEBUG)
    init_file_log(logging.DEBUG)
else:
    init_console_log(logging.CRITICAL)
    init_file_log(logging.WARNING)

# Build all URL using configured services from SERVICES.
logger.debug("Building urls.")
for service in CONFIG['SERVICES']:
    if service != 'index':
        logger.debug("Adding: " + '/rest/' + service + ".")
        # Everything but index is REST.
        APP.add_url_rule('/rest/' + service, service, getattr(views, service),
                         methods=['GET', 'OPTIONS'])
    else:
        logger.debug("Adding: " + "/.")
        APP.add_url_rule('/', 'index', views.index, methods=['GET'])
APP.add_url_rule('/rest/services', 'services', getattr(views, 'services'),
                 methods=['GET', 'OPTIONS'])
