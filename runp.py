#!/bin/python
'''
:since: 06/08/2015
:author: oblivion
'''
from app import APP
from flup.server.fcgi import WSGIServer


if __name__ == '__main__':
    WSGIServer(APP).run()
