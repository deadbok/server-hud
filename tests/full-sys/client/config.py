'''
:since: 03/08/2015
:author: oblivion
'''
from socket import getfqdn, gethostname

SERVER_FIREWALL = 'ws://serverhud-firewall:5000'
SERVER_WEBSERVER = 'ws://serverhud-webserver:5000'

# Dictionary of hosts for the panels on the web page.
HOSTS = {'web_connections': SERVER_WEBSERVER,
         'web_remote_host': SERVER_WEBSERVER,
         'web_uptime': SERVER_WEBSERVER,
         'web_accesses': SERVER_WEBSERVER,
         'fw_connections': SERVER_WEBSERVER,
         'fw_speed': SERVER_FIREWALL}

CLIENT_LOG_FILE = '/home/serverhud/client.log'

DEBUG = True
