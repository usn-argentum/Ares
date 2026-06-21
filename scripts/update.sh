#!/bin/bash
# update.sh
# Pull latest changes, rebuild, reinstall metadata, restart service.
# Run on Jetson after a new commit is pushed.

set -e

WORKSPACE=~/robocup_ws
PACKAGE=rover_drive
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$WORKSPACE/src/$PACKAGE"

echo "[1/4] Pulling latest changes..."
cd "$PACKAGE_DIR"
git pull origin main

echo "[2/4] Building package..."
cd "$WORKSPACE"
colcon build --packages-select "$PACKAGE" --symlink-install
source install/setup.bash

echo "[3/4] Reinstalling Python metadata..."
pip3 install -e "$PACKAGE_DIR" --break-system-packages

echo "[4/4] Restarting service..."
sudo systemctl restart rover_drive

echo ""
echo "Done. Check status with: sudo systemctl status rover_drive"
