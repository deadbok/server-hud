#!/bin/sh

cp /home/vagrant/config.py /home/serverhud/config.py
cp /home/vagrant/serverhud-client.service /lib/systemd/system/.
cp /home/vagrant/serverhud-client.service /lib/systemd/system/.
chmod 664 /lib/systemd/system/serverhud-client.service
systemctl daemon-reload
systemctl enable serverhud-client.service
service serverhud-client start

apt-get install -y curl
