'''
:since: 03/08/2015
:author: oblivion
'''
from socket import getfqdn, gethostname

CLIENT = 'ws://serverhud-client:5000'

# Process to use when calculating uptime.
PROCESS_NAME = "lighttpd"
# Access log of the web server.
ACCESS_LOG = "/var/log/lighttpd/access.log"
# Network interface to use when calculating speed.
INTERFACE = "eth1"
# Port to scan for number of connections
PORT = '80'
# Debug logging.
DEBUG = True
# List of enabled services on this instance.
WS_SERVICES = ['connections', 'uptime', 'remote_host', 'accesses']
# List of allowed host.
ALLOWED = [getfqdn() + ':5000', gethostname() + ':5000', CLIENT]

SERVER_LOG_FILE = '/home/serverhud/server.log'
