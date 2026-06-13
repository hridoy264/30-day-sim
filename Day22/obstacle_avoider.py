"""
Day 22 — Mini-Project: Autonomous Obstacle Avoider (ROS 2 node)
Subscribes to /scan (LiDAR), publishes /cmd_vel to wander while avoiding obstacles.

Run (with ROS 2 sourced, world + robot + bridges running):
    python obstacle_avoider.py
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class ObstacleAvoider(Node):
    def __init__(self):
        super().__init__('obstacle_avoider')
        self.sub = self.create_subscription(LaserScan, '/scan', self.on_scan, 10)
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('Obstacle avoider running. Sense -> Think -> Act.')

    def on_scan(self, msg):
        ranges = [r for r in msg.ranges if r > 0.0]
        if not ranges:
            return
        n = len(msg.ranges)

        # SENSE: distances directly ahead, and left/right halves
        front = [r for r in msg.ranges[n // 2 - 15: n // 2 + 15] if r > 0.0]
        nearest = min(front) if front else 999.0
        left = [r for r in msg.ranges[: n // 2] if r > 0.0]
        right = [r for r in msg.ranges[n // 2:] if r > 0.0]

        cmd = Twist()
        if nearest > 0.8:                 # THINK: path clear?
            cmd.linear.x = 0.4            # ACT: go forward
        else:
            # turn toward the more open side
            turn_dir = 1.0 if (sum(left) / max(len(left), 1)) > \
                              (sum(right) / max(len(right), 1)) else -1.0
            cmd.angular.z = 0.6 * turn_dir
        self.pub.publish(cmd)


def main():
    rclpy.init()
    node = ObstacleAvoider()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
