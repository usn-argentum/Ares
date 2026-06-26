# Ares

ROS2 Jazzy drive package for an Ackermann-steered rover.

# Ares  Run Guide

## How it works

Ares uses ROS2 publish/subscribe to move commands from the operator to the rover.

```
PS5 controller
    │
    ▼ publishes /joy
joy_node (laptop)
    │
    ▼ publishes /cmd_vel
teleop_twist_joy (laptop)
    │
    ▼ subscribes to /cmd_vel, publishes motor topics
rover_drive_node (Jetson)
    │   /left_motor_speed
    │   /right_motor_speed
    │   /left_steering_angle
    │   /right_steering_angle
    ▼ subscribes to all four topics
Hermes / micro-ROS bridge (Teensy)
    │
    ▼
Motor controllers
```

| Node | Machine | Subscribes to | Publishes |
|---|---|---|---|
| `joy_node` | Laptop | — | `/joy` |
| `teleop_twist_joy` | Laptop | `/joy` | `/cmd_vel` |
| `rover_drive_node` | Jetson | `/cmd_vel` | `/left_motor_speed` `/right_motor_speed` `/left_steering_angle` `/right_steering_angle` |
| Hermes (Teensy) | Teensy | all four motor topics | — |

---

## Running

Open four terminals.

**Terminal 1 — Joystick (laptop)**
```bash
cd ~/robocup_ws
source /opt/ros/jazzy/setup.bash
export AMENT_PREFIX_PATH=/home/mar/robocup_ws/install/rover_drive:$AMENT_PREFIX_PATH
ros2 launch rover_drive joystick.launch.py
```

**Terminal 2 — Ares node (laptop)**
```bash
cd ~/robocup_ws
source /opt/ros/jazzy/setup.bash
export AMENT_PREFIX_PATH=/home/mar/robocup_ws/install/rover_drive:$AMENT_PREFIX_PATH
ros2 run rover_drive rover_drive_node
```

**Terminal 3 — micro-ROS agent (Jetson)**
```bash
sudo docker run -it --rm --net=host --privileged microros/micro-ros-agent:jazzy serial --dev /dev/ttyACM0 -b 115200
```

**Terminal 4 — Verify (laptop)**
```bash
source /opt/ros/jazzy/setup.bash
ros2 topic echo /left_motor_speed
```

Hold **L1 + left stick** to send drive commands.
Hold **L1 + right stick** to send steering commands.
