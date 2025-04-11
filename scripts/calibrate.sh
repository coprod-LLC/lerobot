#!/bin/bash

# Default value for arms if not provided
# Usage: ./calibrate.sh "custom_arm_name"
ARMS=${1:-"main_follower"}

python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --robot.cameras='{}' \
  --control.type=calibrate \
  --control.arms="[\"$ARMS\"]"
