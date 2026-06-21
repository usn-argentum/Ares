#!/bin/bash
# launch_joystick.sh
# Run on the operator laptop to start the joystick pipeline.
# Requires: PS5 DualSense connected, ROS_DOMAIN_ID=42, same WiFi as Jetson.
#
# PS5 DualSense mapping (confirmed):
#   Left stick up/down     -> drive  (axis 1)
#   Right stick left/right -> steer  (axis 3)
#   L1                     -> deadman switch (button 4)

source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=42

ros2 run joy joy_node &
ros2 run teleop_twist_joy teleop_node --ros-args \
  -p axis_linear.x:=1 \
  -p scale_linear.x:=1.0 \
  -p scale_linear_turbo.x:=1.0 \
  -p axis_angular.yaw:=3 \
  -p scale_angular.yaw:=1.0 \
  -p enable_button:=4 \
  -p require_enable_button:=true
