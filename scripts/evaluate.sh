#!/bin/bash

REPO_ID_EVAL=${1:-"${HF_USER}/eval_so100_pi0"}
REPO_ID=${2:-"${HF_USER}/so100_pi0"}

python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --control.type=record \
  --control.fps=30 \
  --control.single_task="Grasp a lego block and put it in the bin." \
  --control.repo_id=$REPO_ID_EVAL \
  --control.tags='["tutorial"]' \
  --control.warmup_time_s=5 \
  --control.episode_time_s=30 \
  --control.reset_time_s=30 \
  --control.num_episodes=10 \
  --control.push_to_hub=false \
  --control.policy.path=$REPO_ID_EVAL