from setuptools import setup

package_name = 'rover_drive'

setup(
    name=package_name,
    version='0.5.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name,
         ['package.xml']),
        ('share/' + package_name + '/launch',
         [
             'launch/joystick.launch.py',
             'launch/sim.launch.py',
         ]),
        ('share/' + package_name + '/config',
         [
             'config/joystick.yaml',
         ]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Argentum',
    maintainer_email='',
    description='Ackermann drive node for autonomous rescue rover',
    license='MIT',
    entry_points={
        'console_scripts': [
            'rover_drive_node = rover_drive.rover_drive_node:main',
        ],
    },
)
