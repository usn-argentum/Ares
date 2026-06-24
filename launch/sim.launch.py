import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    """
    Simulation launch file.
    Starts joy_node and teleop_twist_joy only.
<<<<<<< HEAD
    Simulator consumes /cmd_vel directly.
=======
    rover_drive_node is not launched — simulator consumes /cmd_vel directly.
>>>>>>> 8608813ef3726ca761cc7b9d4093b39aee5dd9b4
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
