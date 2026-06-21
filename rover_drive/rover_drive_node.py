import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32


class RoverDriveNode(Node):
    """
    Ackermann drive node.

    Computes per-wheel steering angles and drive speeds from a Twist command
    using Ackermann geometry. Outputs normalized Float32 values on four topics.

    Input:
      /cmd_vel  geometry_msgs/Twist
        linear.x  : drive  [-1.0, +1.0]
        angular.z : steer  [-1.0, +1.0]

    Output:
      /left_motor_speed      std_msgs/Float32  [-1.0, +1.0]
      /right_motor_speed     std_msgs/Float32  [-1.0, +1.0]
      /left_steering_angle   std_msgs/Float32  [-1.0, +1.0]
      /right_steering_angle  std_msgs/Float32  [-1.0, +1.0]
    """

    CMD_VEL_TOPIC     = '/cmd_vel'
    LEFT_SPEED_TOPIC  = '/left_motor_speed'
    RIGHT_SPEED_TOPIC = '/right_motor_speed'
    LEFT_STEER_TOPIC  = '/left_steering_angle'
    RIGHT_STEER_TOPIC = '/right_steering_angle'

    # TODO: Replace with measured values from mechanical team
    WHEELBASE   = 0.4   # m
    TRACK_WIDTH = 0.3   # m
    MAX_STEER   = 30.0  # degrees

    DEADZONE = 0.02

    def __init__(self):
        super().__init__('rover_drive_node')

        self.left_speed_pub  = self.create_publisher(Float32, self.LEFT_SPEED_TOPIC,  10)
        self.right_speed_pub = self.create_publisher(Float32, self.RIGHT_SPEED_TOPIC, 10)
        self.left_steer_pub  = self.create_publisher(Float32, self.LEFT_STEER_TOPIC,  10)
        self.right_steer_pub = self.create_publisher(Float32, self.RIGHT_STEER_TOPIC, 10)

        self.subscription = self.create_subscription(
            Twist,
            self.CMD_VEL_TOPIC,
            self.cmd_vel_callback,
            10
        )

        self.get_logger().info('rover_drive_node started')

    def apply_deadzone(self, value):
        """Suppress joystick drift below threshold."""
        return 0.0 if abs(value) < self.DEADZONE else value

    def clamp(self, value, low=-1.0, high=1.0):
        return max(low, min(high, value))

    def normalize_speeds(self, left, right):
        """Scale speeds so the faster wheel is at +/-1.0, preserving ratio."""
        max_val = max(abs(left), abs(right), 1.0)
        return left / max_val, right / max_val

    def compute_ackermann(self, linear, angular):
        """
        Compute per-wheel speed and steering angle from drive and steer inputs.

        Uses Ackermann geometry: inner wheel turns sharper and drives slower
        than the outer wheel. Angles are normalized by MAX_STEER.
        """
        steer_angle_deg = angular * self.MAX_STEER
        steer_angle_rad = math.radians(steer_angle_deg)

        if abs(steer_angle_rad) < 1e-6:
            return linear, linear, 0.0, 0.0

        R = self.WHEELBASE / math.tan(abs(steer_angle_rad))
        h = self.TRACK_WIDTH / 2.0

        inner_angle = math.degrees(math.atan(self.WHEELBASE / (R - h)))
        outer_angle = math.degrees(math.atan(self.WHEELBASE / (R + h)))

        inner_norm = inner_angle / self.MAX_STEER
        outer_norm = outer_angle / self.MAX_STEER

        if steer_angle_deg > 0:
            left_steer  =  outer_norm
            right_steer =  inner_norm
            left_speed  = linear * (R + h) / R
            right_speed = linear * (R - h) / R
        else:
            left_steer  = -inner_norm
            right_steer = -outer_norm
            left_speed  = linear * (R - h) / R
            right_speed = linear * (R + h) / R

        left_speed, right_speed = self.normalize_speeds(left_speed, right_speed)
        left_steer  = self.clamp(left_steer)
        right_steer = self.clamp(right_steer)

        return left_speed, right_speed, left_steer, right_steer

    def publish(self, l_spd, r_spd, l_str, r_str):
        """Publish all four output topics."""
        msgs = [Float32(), Float32(), Float32(), Float32()]
        vals = [l_spd, r_spd, l_str, r_str]
        pubs = [
            self.left_speed_pub,
            self.right_speed_pub,
            self.left_steer_pub,
            self.right_steer_pub
        ]
        for msg, val, pub in zip(msgs, vals, pubs):
            msg.data = float(val)
            pub.publish(msg)

    def cmd_vel_callback(self, msg):
        linear  = self.apply_deadzone(msg.linear.x)
        angular = self.apply_deadzone(msg.angular.z)

        if linear == 0.0 and angular == 0.0:
            self.publish(0.0, 0.0, 0.0, 0.0)
            self.get_logger().debug('STOP')
            return

        l_spd, r_spd, l_str, r_str = self.compute_ackermann(linear, angular)
        self.publish(l_spd, r_spd, l_str, r_str)

        self.get_logger().debug(
            f'spd=({l_spd:.2f},{r_spd:.2f}) str=({l_str:.2f},{r_str:.2f})'
        )


def main(args=None):
    rclpy.init(args=args)
    node = RoverDriveNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
