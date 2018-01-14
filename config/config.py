'''
:since: 03/08/2015
:author: oblivion
'''
from socket import getfqdn, gethostname

SERVER_MALCOM = 'ws://localhost:5000'
SERVER_STRAYLIGHT = 'ws://localhost:5000'

# Process to use when calculating uptime.
PROCESS_NAME = "lighttpd"
# Access log of the web server.
ACCESS_LOG = "/var/log/lighttpd/access.log"
# Network interface to use when calculating speed.
INTERFACE = "wlp2s0"
# Port to scan for number of connections
PORT = '80'
# Debug logging.
DEBUG = False
# List of enabled services on this instance.
WS_SERVICES = [ 'connections', 'speed', 'uptime',
            'remote_host', 'accesses' ]
# List of allowed host.
ALLOWED = [getfqdn() + ':5000', gethostname() + ':5000', 'localhost']
# Dictionary of hosts for the panels on the web page.
HOSTS = {'web_connections': SERVER_STRAYLIGHT,
         'web_remote_host': SERVER_STRAYLIGHT,
         'web_uptime': SERVER_STRAYLIGHT,
         'web_accesses': SERVER_STRAYLIGHT,
         'fw_connections': SERVER_MALCOM,
         'fw_rcv_speed': SERVER_MALCOM,
         'fw_send_speed': SERVER_MALCOM}

SERVER_LOG_FILE='server.log'
CLIENT_LOG_FILE='client.log'
