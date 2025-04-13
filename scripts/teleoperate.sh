#!/bin/bash

# python lerobot/scripts/control_robot.py   --robot.type=so100   --robot.cameras='{}'   --control.type=teleoperate

python lerobot/scripts/control_robot.py   --robot.type=so100   --control.display_data=true --control.type=teleoperate 
