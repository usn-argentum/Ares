#!/bin/bash
# install_service.sh
# Installs and enables the rover_drive systemd service on the Jetson.
# Run once after cloning the repository.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_FILE="$SCRIPT_DIR/systemd/rover_drive.service"
INSTALL_PATH="/etc/systemd/system/rover_drive.service"

echo "Installing rover_drive service..."
sudo cp "$SERVICE_FILE" "$INSTALL_PATH"
sudo systemctl daemon-reload
sudo systemctl enable rover_drive.service
sudo systemctl start rover_drive.service

echo ""
echo "Service installed. rover_drive_node starts automatically on boot."
echo ""
echo "Commands:"
echo "  sudo systemctl status rover_drive    # status"
echo "  sudo systemctl restart rover_drive   # restart"
echo "  sudo systemctl stop rover_drive      # stop"
echo "  sudo systemctl disable rover_drive   # disable auto-start"
echo "  journalctl -u rover_drive -f         # live logs"
echo "  bash scripts/update.sh               # pull, build, restart"
