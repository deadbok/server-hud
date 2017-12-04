#!/bin/sh

apt-get install plymouth plymouth-themes
cp -Rf /home/vagrant/etc/* /etc/.
update-initramfs -u
update-grub2
