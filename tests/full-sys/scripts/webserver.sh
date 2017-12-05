#!/bin/sh

apt-get install -y lighttpd httperf
gpasswd -a serverhud www-data
lighty-enable-mod accesslog
service lighttpd force-reload
systemctl enable lighttpd
service lighttpd start
