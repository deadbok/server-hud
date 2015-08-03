'''
:since: 03/08/2015
:author: oblivion
'''
# Process to use when calculating uptime.
PROCESS_NAME = "lighttpd"
# Access log of the web server.
ACCESS_LOG = "/var/log/lighttpd/access.log"
# Network interface to use when calculating speed.
INTERFACE = "enp4s0"
# Port to scan for number of connections
PORT = 80
#Debug logging.
DEBUG = True