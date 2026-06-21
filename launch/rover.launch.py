from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    JETSON LAUNCH FILE
    Run this on the Jetson (on the rover).

    Starts:
      - rover_drive_node (Ackermann mixer)

    Subscribes to:
      - /cmd_vel  (received over WiFi from laptop)

    Publishes:
      - /left_motor_speed
      - /right_motor_speed
      - /left_steering_angle
      - /right_steering_angle

    Requirements:
      - Same WiFi network as operator laptop
      - ROS_DOMAIN_ID=42 set on both machines

    Usage:
      ros2 launch rover_drive rover.launch.py
    """

    return LaunchDescription([

        Node(
            package='rover_drive',
            executable='rover_drive_node',
            name='rover_drive_node'
        ),

    ])
