import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    config = os.path.join(
        get_package_share_directory('rover_drive'),
        'config',
        'joystick.yaml'
    )

    return LaunchDescription([

        Node(
            package='joy',
            executable='joy_node',
            name='joy_node'
        ),

        Node(
            package='teleop_twist_joy',
            executable='teleop_node',
            name='teleop_twist_joy',
            parameters=[config]
        ),

        Node(
            package='rover_drive',
            executable='rover_drive_node',
            name='rover_drive_node'
        ),

    ])
