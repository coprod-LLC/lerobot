#!/bin/bash


TASK=${1:-"Grasp a lego block and put it in the bin."}
REPO_ID=${2:-"${HF_USER}/so100_press_red_button_1ep"}

python scripts/control_robot.py \
  --robot.type=so100 \
  --control.type=record \
  --control.fps=30 \
  --control.single_task="$TASK" \
  --control.repo_id="$REPO_ID" \
  --control.tags='["so100","tutorial"]' \
  --control.warmup_time_s=15 \
  --control.episode_time_s=30 \
  --control.reset_time_s=10 \
  --control.num_episodes=1 \
  --control.push_to_hub=true \
  --control.display_data=true