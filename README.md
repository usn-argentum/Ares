# Ares

ROS2 Jazzy drive package for an Ackermann-steered autonomous rescue rover.

Subscribes to `/cmd_vel` and publishes per-wheel motor speed and steering angle
to four output topics consumed by the micro-ROS bridge layer.

---

## Architecture

```
Operator laptop
  scripts/launch_joystick.sh
  └── /cmd_vel ──── WiFi ──► Jetson
                               rover_drive_node (auto-starts on boot)
  joystick.launch.py
  └── /cmd_vel ──── WiFi ──► Jetson
                               rover_drive_node
                               ├── /left_motor_speed
                               ├── /right_motor_speed
                               ├── /left_steering_angle
                               └── /right_steering_angle
                                       │
                                       ▼
                               micro-ROS bridge (Hermes)
                               micro-ROS bridge
                                       │
                                       ▼
                               Motor controllers
```

---

## Interface

### Input
| Topic | Type | Description |
|---|---|---|
| `/cmd_vel` | `geometry_msgs/Twist` | Drive and steer commands |

`linear.x` : drive [-1.0, +1.0]
`angular.z` : steer [-1.0, +1.0]

### Output
| Topic | Type | Range |
|---|---|---|
| `/left_motor_speed` | `std_msgs/Float32` | [-1.0, +1.0] |
| `/right_motor_speed` | `std_msgs/Float32` | [-1.0, +1.0] |
| `/left_steering_angle` | `std_msgs/Float32` | [-1.0, +1.0] |
| `/right_steering_angle` | `std_msgs/Float32` | [-1.0, +1.0] |

> Output ranges are provisional pending interface confirmation from the micro-ROS team.

---

## Steering Model

Ackermann geometry. Front two wheels each drive and steer independently.
Inner wheel turns sharper and drives slower than the outer wheel on a turn.

Geometry constants — update when mechanical team confirms:
```python
WHEELBASE   = 0.4   # m
TRACK_WIDTH = 0.3   # m
MAX_STEER   = 30.0  # degrees
```

---

## Dependencies

```bash
sudo apt install ros-jazzy-joy ros-jazzy-teleop-twist-joy python3-pip
sudo apt install ros-jazzy-joy ros-jazzy-teleop-twist-joy
```

---

## Setup

### Both machines
```bash
mkdir -p ~/robocup_ws/src
cd ~/robocup_ws/src
git clone https://github.com/usn-argentum/Ares.git rover_drive
cd ~/robocup_ws
colcon build --packages-select rover_drive --symlink-install
source /opt/ros/jazzy/setup.bash
colcon build --packages-select rover_drive
source install/setup.bash
echo "export ROS_DOMAIN_ID=42" >> ~/.bashrc
source ~/.bashrc
```

### Jetson — install auto-start service (run once)
```bash
cd ~/robocup_ws/src/rover_drive
bash install_service.sh
```

This installs Python metadata, creates the start script, and enables auto-start on boot.
After installation, `rover_drive_node` starts automatically on boot
and restarts on failure.

---

## Usage

### Operator laptop — start joystick
```bash
bash ~/robocup_ws/src/rover_drive/scripts/launch_joystick.sh
### Operator laptop
```bash
ros2 launch rover_drive joystick.launch.py
```

Hold **L1** to enable. Left stick = drive. Right stick = steer.

### Jetson — service commands
```bash
sudo systemctl status rover_drive    # check status
sudo systemctl restart rover_drive   # restart
sudo systemctl stop rover_drive      # stop
journalctl -u rover_drive -f         # live logs
ros2 topic echo /left_motor_speed    # verify output
```

### After a code update on Jetson
```bash
bash ~/robocup_ws/src/rover_drive/scripts/update.sh
```

bash scripts/update.sh
```

Pulls latest changes, rebuilds, and restarts the service in one command.

### Simulation
```bash
ros2 launch rover_drive sim.launch.py
```

---

## PS5 DualSense Mapping

| Input | Axis/Button | ROS field |
|---|---|---|
| Left stick up/down | Axis 1 | `linear.x` |
| Right stick left/right | Axis 3 | `angular.z` |
| L1 | Button 4 | Deadman switch |

---

## Known Issue — ROS2 Package Registration

On Ubuntu 24 with setuptools 68, `ros2 run` and `ros2 launch rover_drive` may
fail with `Package 'rover_drive' not found`. This is a known ROS2 Jazzy issue.

**Workaround (applied by install_service.sh automatically):**
```bash
pip3 install -e . --break-system-packages
```

Use `scripts/launch_joystick.sh` instead of `ros2 launch rover_drive joystick.launch.py`
on the laptop.

---

## Status

| Item | Status |
|---|---|
| Ackermann drive node | Done |
| PS5 joystick teleoperation | Done |
| Multi-machine WiFi | Done |
| Jetson auto-start | Done |
| Rover geometry | Pending mechanical team |
| micro-ROS interface | Pending |
| URDF / simulation | Pending rover geometry |
| Autonomous navigation | Planned |
