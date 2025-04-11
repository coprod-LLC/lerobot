#!/bin/bash

echo "remap the device serial port(ttyACMx) to /dev/so-100/follower_right"
echo "start copy follower_right.rules to  /etc/udev/rules.d/"
sudo cp follower_right.rules  /etc/udev/rules.d
echo " "
echo "Restarting udev"
echo ""
sudo service udev reload
sudo service udev restart
echo "finish "