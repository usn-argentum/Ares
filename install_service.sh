#!/bin/bash
# install_service.sh
# Run once on the Jetson after cloning the repository.
# Installs Python metadata, creates the start script, and enables auto-start.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
USERNAME=$(whoami)
HOME_DIR="/home/$USERNAME"

echo "[1/4] Installing Python package metadata..."
pip3 install -e "$SCRIPT_DIR" --break-system-packages

echo "[2/4] Creating start script..."
cat > "$HOME_DIR/start_rover.sh" << INNEREOF
#!/bin/bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=42
export PYTHONPATH=$HOME_DIR/robocup_ws/install/rover_drive/lib/python3.12/site-packages:\$PYTHONPATH
exec $HOME_DIR/robocup_ws/install/rover_drive/lib/rover_drive/rover_drive_node
INNEREOF
chmod +x "$HOME_DIR/start_rover.sh"

echo "[3/4] Installing systemd service..."
SERVICE_FILE="$SCRIPT_DIR/systemd/rover_drive.service"
INSTALL_PATH="/etc/systemd/system/rover_drive.service"
sudo cp "$SERVICE_FILE" "$INSTALL_PATH"
sudo sed -i "s|User=argentum|User=$USERNAME|g" "$INSTALL_PATH"
sudo sed -i "s|/home/argentum|$HOME_DIR|g" "$INSTALL_PATH"
sudo systemctl daemon-reload
sudo systemctl enable rover_drive.service
sudo systemctl start rover_drive.service

echo "[4/4] Done."
echo ""
echo "rover_drive_node starts automatically on boot."
echo ""
echo "Commands:"
echo "  sudo systemctl status rover_drive    # status"
echo "  sudo systemctl restart rover_drive   # restart"
echo "  sudo systemctl stop rover_drive      # stop"
echo "  sudo systemctl disable rover_drive   # disable auto-start"
echo "  journalctl -u rover_drive -f         # live logs"
echo "  bash scripts/update.sh               # pull, build, restart"
