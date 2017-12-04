#!/bin/sh

cp -RT /home/vagrant/opt /opt
cp /home/vagrant/opt/kiosk/.bash_logout /home/serverhud/.bash_logout
cp /home/vagrant/opt/kiosk/.bashrc /home/serverhud/.bashrc
cp /home/vagrant/opt/kiosk/.profile /home/serverhud/.profile
cp /home/vagrant/opt/kiosk/.xsessionrc /home/serverhud/.xsessionrc
cp /home/vagrant/config.py /opt/kiosk/config.py

chown -R serverhud:serverhud /home/serverhud/*
