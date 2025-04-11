#!/bin/bash

echo "remap the device serial port(ttyACMx) to /dev/so-100/leader_left"
echo "start copy leader_left.rules to  /etc/udev/rules.d/"
sudo cp leader_left.rules  /etc/udev/rules.d
echo " "
echo "Restarting udev"
echo ""
sudo service udev reload
sudo service udev restart
echo "finish "