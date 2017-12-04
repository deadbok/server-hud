#!/bin/sh

apt-get install -y lighttpd
gpasswd -a serverhud www-data
systemctl enable lighttpd
service lighttpd start
