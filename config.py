'''
:since: 03/08/2015
:author: oblivion
'''
from socket import getfqdn, gethostname

SERVER_MALCOM = 'http://malcom.groenholdt.net:5000'
SERVER_STRAYLIGHT = 'http://straylight.groenholdt.net:5000'

# Process to use when calculating uptime.
PROCESS_NAME = "lighttpd"
# Access log of the web server.
ACCESS_LOG = "/var/log/lighttpd/access.log"
# Network interface to use when calculating speed.
INTERFACE = "enp4s0"
# Port to scan for number of connections
PORT = '80'
# Debug logging.
DEBUG = True
# List of enabled services on this instance.
SERVICES = ['index', 'connections', 'rcv_speed', 'send_speed', 'uptime',
            'remote_host', 'accesses']
# List of allowed host.
ALLOWED = [getfqdn() + ':5000', gethostname() + ':5000']
# Dictionary of hosts for the panels on the web page.
HOSTS = {'web_connections': SERVER_STRAYLIGHT,
         'web_remote_host': SERVER_STRAYLIGHT,
         'web_uptime': SERVER_STRAYLIGHT,
         'web_accesses': SERVER_STRAYLIGHT,
         'fw_connections': SERVER_MALCOM,
         'fw_rcv_speed': SERVER_MALCOM,
         'fw_send_speed': SERVER_MALCOM}
