#!/bin/bash

echo "delete remap the device serial port(ttyACMx) to /dev/so-100/follower_right"
echo "sudo rm   /etc/udev/rules.d/follower_right.rules"
sudo rm   /etc/udev/rules.d/follower_right.rules
echo " "
echo "Restarting udev"
echo ""
sudo service udev reload
sudo service udev restart
echo "finish  delete"