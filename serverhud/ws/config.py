'''
:since: 10/09/2016
:author: oblivion
'''
import os
import types


CONFIG = None


def read_config(config_filename=None):
    global CONFIG

    CONFIG = dict()
    if config_filename is None:
        config_filename = os.getcwd() + '/config.py'
    d = types.ModuleType(config_filename)
    d.__file__ = config_filename
    try:
        with open(config_filename) as config_file:
            exec(compile(config_file.read(), config_filename, 'exec'), d.__dict__)
    except IOError as e:
        e.strerror = 'Unable to load configuration file (%s)' % e.strerror
        raise
    if isinstance(d, str):
            d = import_string(d)
    for key in dir(d):
        if key.isupper():
            CONFIG[key] = getattr(d, key)
    return CONFIG


def init_config(path=None):
    read_config(path)
