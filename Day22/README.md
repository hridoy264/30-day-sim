# Day 22 — 🛠 Mini-Project: A Robot That Explores a World

## 🎯 Today's Goal
Bring the entire Gazebo phase together: write a ROS 2 node that reads the robot's LiDAR and autonomously drives it around your world while avoiding obstacles. Your first **autonomous** robot behavior.

---

## Overview

This is the Phase 4 capstone. You'll write a real ROS 2 node — the kind that runs on actual robots — that **subscribes** to LiDAR scans and **publishes** velocity commands to avoid walls. This "sense → think → act" loop is the foundation of all autonomy. Simple obstacle avoidance today; the same structure scales to full navigation systems.

---

## The Autonomy Loop

Every autonomous robot runs this loop, and you'll implement it:

```
   ┌─────────────────────────────┐
   │  SENSE  → read LiDAR (/scan) │
   │  THINK  → decide: turn/go?   │
   │  ACT    → publish /cmd_vel   │
   └──────────────┬──────────────┘
                  └── repeat forever
```

---

## The Logic: Reactive Obstacle Avoidance

A simple, effective rule:

- Look at the LiDAR distances **in front** of the robot.
- If the path ahead is **clear** → drive forward.
- If something is **close ahead** → stop going forward and **turn** until it's clear.

That's it. No maps, no planning — just react to what you sense. It's surprisingly capable and teaches the core pattern.

---

## The ROS 2 Node

See `obstacle_avoider.py`. The essential structure of a ROS 2 Python node:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoider(Node):
    def __init__(self):
        super().__init__('obstacle_avoider')
        # SENSE: subscribe to the LiDAR
        self.sub = self.create_subscription(LaserScan, '/scan', self.on_scan, 10)
        # ACT: publisher for velocity
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def on_scan(self, msg):
        # look at the slice of beams directly ahead
        n = len(msg.ranges)
        front = msg.ranges[n//2 - 15 : n//2 + 15]
        front = [r for r in front if r > 0.0]
        nearest = min(front) if front else 999.0

        cmd = Twist()
        if nearest > 0.8:           # THINK: clear ahead?
            cmd.linear.x = 0.4      # go
        else:
            cmd.angular.z = 0.6     # turn to avoid
        self.pub.publish(cmd)       # ACT

def main():
    rclpy.init()
    rclpy.spin(ObstacleAvoider())

if __name__ == '__main__':
    main()
```

Recognize the parts from the whole phase: subscribing to a sensor (Day 20), publishing `/cmd_vel` (Day 19), and the node/topic structure (Day 18). It all converges here.

---

## Running It

1. Launch your world + robot + sensor bridges (build a launch file from Day 18's pattern).
2. Make sure `/scan` and `/cmd_vel` are bridged and Gazebo is **playing**.
3. Run your node:
   ```bash
   python obstacle_avoider.py
   ```
4. Watch the robot drive itself, slow near obstacles, turn away, and continue. Open **RViz** (Day 21) alongside to *see* the LiDAR reasoning live.

---

## 📝 Today's Task

1. Get `obstacle_avoider.py` running and watch the robot explore autonomously.
2. **Tune behavior:** change the `0.8 m` threshold and the forward/turn speeds — find a smooth wander.
3. **Smarter turns:** compare the average distance on the left vs. right half of the scan and turn toward the *more open* side.
4. Add obstacles to your Day-17 world and confirm the robot avoids the new ones.
5. **Reflect:** in your log, describe how "sense → think → act" appears in your code.

---

## 🏆 Phase 4 Complete!

You can now install Gazebo + ROS 2, build worlds and robots in SDF, add sensors, bridge to ROS 2, visualize in RViz, and write autonomous nodes. This is the professional robotics simulation stack — a serious, job-relevant skill set. Outstanding work.

---

## ✅ Key Takeaways

✓ Autonomy is a loop: **sense (LiDAR) → think (decide) → act (`/cmd_vel`)**, repeated forever.

✓ A ROS 2 node **subscribes** to sensors and **publishes** commands — the real-robot software pattern.

✓ **Reactive avoidance** (turn when something's close ahead) needs no map yet is genuinely capable.

✓ This project fuses the whole phase: SDF robot, sensors, bridge, nodes, and RViz.

✓ The same structure scales up to full navigation stacks (e.g., Nav2).

---

## 📚 References & Resources

- [Writing a ROS 2 Python node](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
- [sensor_msgs/LaserScan](https://docs.ros.org/en/api/sensor_msgs/html/msg/LaserScan.html)
- [Nav2 — the ROS 2 navigation stack (where this leads)](https://docs.nav2.org/)

---

## 🔭 What's Next?

**Day 23 — Intro to Reinforcement Learning.** New phase! Instead of *programming* behavior, we'll teach robots to *learn* it themselves — starting with the Gymnasium framework and the CartPole you already understand.

---

*"You wrote code that decides for itself. That's the first step from automation to autonomy."*
