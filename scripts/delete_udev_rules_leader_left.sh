#!/bin/bash

echo "delete remap the device serial port(ttyACMx) to /dev/so-100/leader_left"
echo "sudo rm   /etc/udev/rules.d/leader_left.rules"
sudo rm   /etc/udev/rules.d/leader_left.rules
echo " "
echo "Restarting udev"
echo ""
sudo service udev reload
sudo service udev restart
echo "finish  delete"