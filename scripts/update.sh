#!/bin/bash
# update.sh
# Pull latest changes, rebuild package, restart service.
# Run on Jetson after pushing a new commit.

set -e

WORKSPACE=~/robocup_ws
PACKAGE=rover_drive

echo "[1/3] Pulling latest changes..."
cd "$WORKSPACE/src/$PACKAGE"
git pull origin main

echo "[2/3] Building package..."
cd "$WORKSPACE"
colcon build --packages-select "$PACKAGE"
source install/setup.bash

echo "[3/3] Restarting service..."
sudo systemctl restart rover_drive

echo ""
echo "Done. Check status with: sudo systemctl status rover_drive"
