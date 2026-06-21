import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    """
    Operator laptop launch file.
    Starts joy_node and teleop_twist_joy. Publishes /cmd_vel over WiFi.

    Note: If ros2 launch fails due to package registration issues,
    use scripts/launch_joystick.sh instead.
    """

    config = os.path.join(
        get_package_share_directory('rover_drive'),
        'config',
        'joystick.yaml'
    )

    return LaunchDescription([
        Node(package='joy', executable='joy_node', name='joy_node'),
        Node(
            package='teleop_twist_joy',
            executable='teleop_node',
            name='teleop_twist_joy',
            parameters=[config]
        ),
    ])
