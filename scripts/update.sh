#!/bin/bash
# update.sh
# Pull latest changes, rebuild, reinstall metadata, restart service.
# Run on Jetson after a new commit is pushed.
# Pull latest changes, rebuild package, restart service.
# Run on Jetson after pushing a new commit.

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
