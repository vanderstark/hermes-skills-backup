---
title: "Drone Development — End-to-End ROS 2 Build & Autonomous Flight"
description: "Comprehensive guide for building, simulating, and flying autonomous drones using ROS 2, ArduPilot, PX4, and Gazebo. Covers hardware selection, flight control stack, perception pipelines, and deployment on real quadrotors."
trigger: "Use when: building a drone from scratch, setting up ROS 2 flight stack, simulating multi-drone scenarios, developing autonomous flight controllers, implementing obstacle avoidance, or deploying code to PX4-based flight controllers."
tags: ["ros2", "drone", "uav", "autopilot", "px4", "gazebo", "quadrotor", "autonomous", "robotics"]
version: "1.0.0"
---

# 🚁 Drone Development — Comprehensive Guide

Build, simulate, and fly autonomous drones end-to-end with ROS 2, ArduPilot, PX4, and Gazebo Harmonic.

---

## 📋 Overview

This skill combines **3 complementary approaches** for complete drone mastery:

1. **ROS 2 + ArduPilot + Gazebo** — simulation-first learning & multi-drone scenarios
2. **ROS 2 + PX4 Control** — autonomous flight controllers with odometry & self-check
3. **Advanced Flight Controllers** — PhD-level control theory for real hardware

**Covers entire lifecycle:**
- Hardware selection (flight controller, frame, sensors)
- Software stack setup (ROS 2, PX4, ArduPilot, Gazebo)
- Simulation environment (digital twin testing)
- Autonomous control algorithms
- Real hardware deployment & flight testing

---

## 🎯 Prerequisites

### Hardware Stack (For Real Drone)
- **Flight Controller:** Pixhawk 4/5, ArduPilot compatible
- **Frame:** DIY quadcopter or commercial frame
- **Motors & ESCs:** Brushless + electronic speed controllers
- **Sensors:** IMU, GPS, barometer, optional LiDAR/camera
- **Power:** LiPo battery, voltage regulators
- **Comms:** telemetry link (433MHz or 2.4GHz)

### Software Stack (Linux/Ubuntu 22.04+)
- ROS 2 (Humble or Jazzy)
- PX4 Autopilot firmware
- ArduPilot firmware (alternative)
- Gazebo Harmonic simulator
- QGroundControl (ground station)
- Python 3.8+, Colcon build tools

---

## 🏗️ Part 1: Setup ROS 2 + Gazebo Simulation Environment

### Step 1: Install ROS 2 & Dependencies

```bash
# Install ROS 2 Humble (Ubuntu 22.04)
curl https://repo.ros2.org/ros.key | sudo apt-key add -
sudo sh -c 'echo "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'
sudo apt update
sudo apt install ros-humble-desktop

# Install Gazebo Harmonic
sudo apt install gazebo
sudo apt install ros-humble-gazebo-ros

# Install colcon build tools
sudo apt install python3-colcon-common-extensions
```

### Step 2: Create ROS 2 Workspace

```bash
mkdir -p ~/drone_ws/src
cd ~/drone_ws
colcon build

# Source workspace
source install/setup.bash
```

### Step 3: Install Drone Simulation Stack

```bash
cd ~/drone_ws/src

# Clone PX4-Autopilot with Gazebo plugin
git clone https://github.com/PX4/PX4-Autopilot.git
cd PX4-Autopilot
make px4_sitl gazebo-classic

# Clone ArduPilot (alternative)
git clone https://github.com/ArduPilot/ardupilot.git
cd ardupilot
./Tools/autotest/sim_vehicle.py -v ArduCopter -f quad
```

### Step 4: Launch Multi-Drone Simulation (Gazebo)

```bash
# Launch Gazebo with 3 drones
gazebo /opt/ros/humble/share/px4_gazebo/worlds/empty.world
```

---

## 🔧 Part 2: ROS 2 Flight Control Stack (PX4)

### Autonomous Flight Node Architecture

```
┌─────────────────────────────────────┐
│      High-Level Mission Planner     │  (Python/C++)
├─────────────────────────────────────┤
│   ROS 2 Control Bridge (sverk-ros2) │
│   - Odometry estimation             │
│   - Self-check diagnostics          │
│   - MAVLink communication            │
├─────────────────────────────────────┤
│     PX4 Autopilot Firmware          │
│   - Flight controllers              │
│   - Sensor fusion                   │
│   - Motor command output            │
├─────────────────────────────────────┤
│   Hardware (Motors, Sensors, ESCs)  │
└─────────────────────────────────────┘
```

### Create ROS 2 Flight Control Node

**File: `src/drone_control/src/autonomous_controller.py`**

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, TwistStamped
from sensor_msgs.msg import Imu
from px4_msgs.msg import VehicleCommand, OffboardControlMode
import numpy as np

class AutonomousFlightController(Node):
    def __init__(self):
        super().__init__('autonomous_flight_controller')
        
        # PX4 publishers
        self.cmd_pub = self.create_publisher(
            VehicleCommand, '/fmu/in/vehicle_command', 10)
        self.offboard_pub = self.create_publisher(
            OffboardControlMode, '/fmu/in/offboard_control_mode', 10)
        
        # Subscribers
        self.pose_sub = self.create_subscription(
            PoseStamped, '/fmu/out/vehicle_local_position/pose', 
            self.pose_callback, 10)
        self.imu_sub = self.create_subscription(
            Imu, '/fmu/out/imu', self.imu_callback, 10)
        
        # State
        self.current_pose = None
        self.target_pose = np.array([0.0, 0.0, -5.0])  # x, y, z (NED)
        
        # Control loop
        self.timer = self.create_timer(0.05, self.control_loop)
        
    def pose_callback(self, msg):
        self.current_pose = np.array([
            msg.pose.position.x,
            msg.pose.position.y,
            msg.pose.position.z
        ])
    
    def imu_callback(self, msg):
        pass  # Log IMU data if needed
    
    def control_loop(self):
        if self.current_pose is None:
            return
        
        # Simple PD controller to target position
        error = self.target_pose - self.current_pose
        control = 0.5 * error  # Proportional term
        
        # Publish offboard mode
        offboard_msg = OffboardControlMode()
        offboard_msg.position = True
        offboard_msg.velocity = False
        offboard_msg.acceleration = False
        self.offboard_pub.publish(offboard_msg)
        
        # Publish control command
        # (send to position setpoint via MAVLink)
        self.get_logger().info(f"Position: {self.current_pose}, Error: {error}")

def main(args=None):
    rclpy.init(args=args)
    controller = AutonomousFlightController()
    rclpy.spin(controller)

if __name__ == '__main__':
    main()
```

### Launch File

**File: `src/drone_control/launch/autonomous_flight.launch.py`**

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='drone_control',
            executable='autonomous_controller',
            name='flight_controller',
            output='screen'
        ),
    ])
```

---

## 🎨 Part 3: Perception Pipeline (LiDAR/Camera)

### Obstacle Avoidance with LiDAR

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import numpy as np

class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10)
        self.min_distance = 1.0  # meters
        self.threat_detected = False
        
    def scan_callback(self, msg):
        ranges = np.array(msg.ranges)
        self.threat_detected = np.min(ranges) < self.min_distance
        
        if self.threat_detected:
            self.get_logger().warn(f"Obstacle detected at {np.min(ranges):.2f}m")
            # Trigger avoidance maneuver

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidanceNode()
    rclpy.spin(node)
```

---

## 🧪 Part 4: Testing & Validation

### Simulation Testing (Gazebo)

```bash
# Launch SITL simulation with ROS 2 bridge
export GAZEBO_PLUGIN_PATH=$GAZEBO_PLUGIN_PATH:~/drone_ws/install/px4_gazebo/lib
gazebo-gui ~/drone_ws/install/px4_gazebo/share/px4_gazebo/worlds/empty.world

# In separate terminal: launch ROS 2 controller
source ~/drone_ws/install/setup.bash
ros2 launch drone_control autonomous_flight.launch.py
```

### Unit Tests

```bash
colcon test --packages-select drone_control
colcon test-result --verbose
```

### Flight Testing Checklist

- [ ] Propeller balance check
- [ ] Motor spin test (no propellers!)
- [ ] Sensor calibration (compass, accelerometer, gyro)
- [ ] Radio range test
- [ ] Failsafe configuration
- [ ] Hover test (manual mode, tether)
- [ ] Autonomous flight (geofenced area)

---

## 📚 GitHub Resources (Comprehensive)

### Recommended Repositories

1. **ROS 2 + ArduPilot + Gazebo Tutorial** (21 stars)
   - https://github.com/AbdullahArpaci/ros2-ardupilot-gazebo-harmonic-drone-simulation-tutorial
   - **Best for:** Multi-drone simulation, learning ArduPilot with ROS 2
   - Setup multi-drone scenarios in Gazebo Harmonic

2. **PX4 ROS 2 Control Stack** (1 star)
   - https://github.com/last1162/sverk-ros2
   - **Best for:** Autonomous flight control with odometry feedback
   - Built-in self-check diagnostics for autonomous systems

3. **Advanced Flight Controller Research** (2 stars)
   - https://github.com/evannsmc/evannsmc
   - **Best for:** PhD-level control theory, real quadrotor deployment
   - Provably safe autonomous flight controllers

---

## 🔄 Workflow: From Simulation to Hardware

### Phase 1: Simulation (Gazebo SITL)
```
Design → Simulate → Validate → Debug
```
- Test control algorithms in Gazebo
- Verify multi-drone interactions
- Tune PID gains

### Phase 2: Hardware-in-Loop (HITL)
```
Gazebo ←→ Flight Controller (via serial/USB)
```
- Run real firmware with simulated sensors
- Test telemetry integration
- Validate MAVLink communication

### Phase 3: Real Flight Testing
```
Real Drone → Sensors → Flight Controller → Motors
```
- Start with manual mode (RC joystick)
- Switch to offboard autonomous mode
- Monitor telemetry in real-time

---

## ⚙️ Advanced Topics

### Multi-Drone Coordination
- Formation flying (swarms)
- Distributed consensus algorithms
- Collision avoidance between teammates

### Computer Vision
- Object detection (YOLOv8)
- Visual odometry (monocular/stereo)
- Autonomous landing on visual markers

### Machine Learning
- Reinforcement learning for flight policies
- Imitation learning from expert trajectories
- Anomaly detection in sensor data

---

## 🚨 Safety Checklist

### Pre-Flight
- [ ] All propellers intact & balanced
- [ ] Battery fully charged
- [ ] GPS lock acquired
- [ ] RC link functioning
- [ ] Failsafe configured (return-to-home)

### During Flight
- [ ] Operator at flight controls (RC remote ready)
- [ ] Observer watching drone
- [ ] Designated airspace clear of people
- [ ] Telemetry being logged
- [ ] Emergency stop (kill switch) accessible

### Post-Flight
- [ ] Battery cooled before storage
- [ ] Log files analyzed for anomalies
- [ ] Propellers inspected for damage

---

## 📖 Reference Documentation

| Resource | Link |
|----------|------|
| PX4 Developer Guide | https://docs.px4.io/main/en/ |
| ArduPilot Documentation | https://ardupilot.org/copter/ |
| ROS 2 Humble Docs | https://docs.ros.org/en/humble/ |
| Gazebo Harmonic | https://gazebosim.org/docs/harmonic/ |
| MAVLink Protocol | https://mavlink.io/ |

---

## 🛠️ Troubleshooting

### Problem: "No GPS Lock"
**Solution:** Verify GPS module connected, check RF interference, restart GPS.

### Problem: "Motors not spinning"
**Solution:** Check ESC calibration (full throttle range), verify motor connections, test with safe propeller guards.

### Problem: "Drone drifts in hover"
**Solution:** Recalibrate accelerometer, adjust PID gains (increase P term), check propeller balance.

### Problem: "ROS 2 node crashes on startup"
**Solution:** `source install/setup.bash`, verify MAVLink port open, check PX4 firmware version compatibility.

---

## 🎓 Learning Path

### Week 1-2: Fundamentals
- Study ROS 2 basics (topics, services, actions)
- Install Gazebo simulation
- Launch multi-drone scenarios

### Week 3-4: Control Theory
- Learn PID controller tuning
- Study attitude control vs position control
- Implement simple autonomous mission

### Week 5-6: Real Hardware
- Assemble quadrotor frame
- Flash PX4 firmware
- Perform static ground tests

### Week 7-8: Flight Testing
- First manual flights (tethered)
- Autonomous waypoint missions
- Obstacle avoidance (if LiDAR equipped)

---

## 📞 Getting Help

1. **Simulation Issues** → Check Gazebo simulation node stability
2. **Control Issues** → Review PID tuning guide, check sensor calibration
3. **ROS 2 Issues** → Verify DDS configuration, check network connectivity
4. **Firmware Issues** → Consult PX4/ArduPilot documentation

**Community Forums:**
- PX4 Discuss: https://discuss.px4.io/
- ArduPilot Forum: https://discuss.ardupilot.org/
- ROS Discourse: https://discourse.ros.org/

---

**Ready to build your autonomous drone fleet, Bos?** 🚁🙏
