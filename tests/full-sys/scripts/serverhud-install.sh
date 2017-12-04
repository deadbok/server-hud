#!/bin/sh

apt-get update
apt-get install -y python3-pip
pip3 install --upgrade --force-reinstall /home/vagrant/serverhud-$1-py3-none-any.whl
