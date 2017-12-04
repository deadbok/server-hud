#!/bin/sh

cp /home/vagrant/config.py /home/serverhud/config.py
cp /home/vagrant/serverhud-server.service /lib/systemd/system/.
chmod 664 /lib/systemd/system/serverhud-server.service
systemctl daemon-reload
systemctl enable serverhud-server.service
service serverhud-server start
