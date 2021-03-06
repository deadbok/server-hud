'''
Log module.

:since: 22 Aug 2011
:author: oblivion
'''
from logging import handlers
import logging
import sys


logger = logging.getLogger("server-hud-ws")
'''Our Logger object'''

# logger.setLevel(logging.DEBUG)

console_log = logging.StreamHandler(sys.stdout)
'''Handler for logging to the console.'''

def init_file_log(level=logging.DEBUG, path=None):
    '''Initialise the file logging.

    :param level: The level at which the message is logged to the file.
    :type level: logging level
    '''
    if path is None:
        path = "/var/log/server-hud-ws.log"
    file_log = handlers.RotatingFileHandler(path,
                                       maxBytes=10000000,
                                       backupCount=5)
    file_log.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s'))
    logger.addHandler(file_log)
    file_log.doRollover()
    file_log.setLevel(level)


class ConsoleFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(self, '%(message)s')

    def format(self, record):
        '''
        Format function to emphasise errors.

        :type record: LogRecord
        :param record: The log record to format.
        :rtype: str
        :return: The resulting string'''
        if record.levelno >= logging.WARNING:
            logging.Formatter.__init__(self, '%(levelname)s: %(message)s')
        else:
            logging.Formatter.__init__(self, '%(message)s')
        msg = logging.Formatter.format(self, record)
        return msg


def init_console_log(level=logging.INFO):
    '''
    Initialise the console logging.

    @type level: logging level
    @param level: The level at which the message is logged to the console.
    '''
    console_log.setLevel(level)
    console_log.setFormatter(ConsoleFormatter())
    logger.addHandler(console_log)


def close_log():
    '''Close all logs.'''
    console_log.close()
    file_log.close()
