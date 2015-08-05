'''
:since: 01/08/2015
:author: oblivion
'''
import logging

from flask import Flask

from app.log import logger, init_file_log, init_console_log, close_log


APP = Flask(__name__)
APP.config.from_object('config')

if APP.config['DEBUG']:
    init_console_log(logging.DEBUG)
    init_file_log(logging.DEBUG)
else:
    init_console_log(logging.CRITICAL)
    init_file_log(logging.WARNING)

from app import views  #@NoMove

views.build_urls()
