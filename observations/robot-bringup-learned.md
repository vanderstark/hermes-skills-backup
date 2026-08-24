# Learning Observation: Robot Bringup (ROS2)

**Skill:** `robotics-agent-robot-bringup`
**Date:** 2026-08-24
**Learner:** Hermes Agent (for Bos - Polri, Drone Development)
**Status:** ACTIVE LEARNING

---

## 🔍 Skill Overview

This skill covers patterns and best practices for bringing up a complete ROS2-based robotics system on a robot's onboard computer. It includes systemd services, launch file composition, ordered startup, and production monitoring.

Key concepts:
- **systemd service units** for ROS2 launch
- **Launch file composition** for modular robot stacks
- **Ordered startup with health checks** to avoid race conditions
- **udev rules** for deterministic device naming
- **Network configuration** for multi-machine ROS2
- **Watchdog and heartbeat monitoring** for production systems

Covers Ubuntu 22.04/24.04 with ROS2 Humble, Iron, and Jazzy.

---

## 🧠 Conceptual Architecture

### The Robot Bringup Stack (Layered)

```
┌───────────────────────────────────────────────┐
│              APPLICATION LAYER                 │
│  Navigation, manipulation, mission planning    │
├───────────────────────────────────────────────┤
│              PERCEPTION LAYER                  │
│  Object detection, SLAM, point cloud filtering │
├───────────────────────────────────────────────┤
│               DRIVER LAYER                     │
│  Camera drivers, LiDAR drivers, motor control  │
├───────────────────────────────────────────────┤
│             HARDWARE LAYER                     │
│  udev rules, device enumeration, USB reset     │
├───────────────────────────────────────────────┤
│            ROS2 ENVIRONMENT                    │
│  Source workspace, set RMW, ROS_DOMAIN_ID    │
├───────────────────────────────────────────────┤
│       SYSTEMD TARGETS & SERVICES               │
│  network-online.target → robot-hw.target →     │
│  robot-bringup.target                        │
└───────────────────────────────────────────────┘
```
```
LINUX BOOT (systemd)
    ↓
HARDWARE BOOT
```

---

## 🛠️ systemd Service Units for ROS2

### 1. Basic ROS2 Service Unit Template

```ini
# /etc/systemd/system/robot-bringup.service
[Unit]
Description=Robot ROS2 Bringup Stack
Documentation=https://github.com/my-org/my-robot
After=network-online.target robot-hw.target
Wants=network-online.target
Requires=robot-hw.target

[Service]
Type=notify
User=robot
Group=robot
WorkingDirectory=/home/robot

# Load ROS2 environment variables from a dedicated env file
EnvironmentFile=/etc/robot/ros2.env

# Pre-start check: verify critical devices exist
ExecStartPre=/usr/local/bin/robot-device-check.sh

# Start the ROS2 launch file via bash so we can source the workspace
ExecStart=/bin/bash -c 'source /opt/ros/${ROS_DISTRO}/setup.bash && source /home/robot/ros2_ws/install/setup.bash && exec ros2 launch my_robot bringup.launch.py'

# Graceful shutdown: send SIGINT first (Ctrl+C equivalent for ROS2)
ExecStop=/bin/kill -INT $MAINPID
TimeoutStopSec=30

# Restart on failure, but not on clean exit
Restart=on-failure
RestartSec=5

# systemd watchdog: service must call sd_notify(WATCHDOG=1) within this interval
WatchdogSec=30

# Process management
KillMode=mixed
KillSignal=SIGINT
FinalKillSignal=SIGKILL
TimeoutStartSec=60

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=robot-bringup

[Install]
WantedBy=multi-user.target
```

### 2. Environment Setup in systemd

Create `/etc/robot/ros2.env`:

```bash
# ROS2 distribution
ROS_DISTRO=humble

# DDS middleware selection
RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Domain isolation: unique per robot to avoid cross-talk
ROS_DOMAIN_ID=42

# CycloneDDS configuration file path
CYCLONEDDS_URI=file:///etc/robot/cyclonedds.xml

# Disable localhost-only mode for multi-machine setups
ROS_LOCALHOST_ONLY=0

# Logging configuration
ROS_LOG_DIR=/var/log/ros2
RCUTILS_LOGGING_USE_STDOUT=0
RCUTILS_COLORIZED_OUTPUT=0

# Robot-specific configuration
ROBOT_NAME=my_robot_01
ROBOT_CONFIG_DIR=/etc/robot/config
```

---

## 🎯 Launch File Composition (Layered)

### Hardware Layer (`hardware.launch.py`)
```python
# my_robot_bringup/launch/hardware.launch.py
from launch import LaunchDescription
from launch.actions import LogInfo, ExecuteProcess, TimerAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, EnvironmentVariable

def generate_launch_description():
    robot_name = LaunchConfiguration('robot_name',
        default=EnvironmentVariable('ROBOT_NAME', default_value='default_robot'))

    check_camera = ExecuteProcess(
        cmd=['test', '-e', '/dev/robot/camera_front'],
        name='check_camera_front',
        output='screen',
    )

    check_lidar = ExecuteProcess(
        cmd=['test', '-e', '/dev/robot/lidar'],
        name='check_lidar',
        output='screen',
    )

    log_ready = TimerAction(
        period=2.0,
        actions=[LogInfo(msg='Hardware checks passed, devices ready')],
    )

    return LaunchDescription([
        check_camera, check_lidar, log_ready,
    ])
```

### Driver Layer (`drivers.launch.py`)
Camera, LiDAR, IMU, motor drivers with health checks.

### Perception Layer (`perception.launch.py`)
SLAM, detection, sensor fusion using composable node containers.

### Application Layer (`application.launch.py`)
Navigation, planning, mission.

### Top-Level Bringup (`bringup.launch.py`)
Composes all layers with conditional arguments:

```python
# bringup.launch.py - Top-level
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    use_sim = LaunchConfiguration('use_sim')
    enable_perception = LaunchConfiguration('enable_perception')

    hardware_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution(
            [FindPackageShare('my_robot_bringup'), 'launch', 'hardware.launch.py']
        )), condition=UnlessCondition(use_sim),
    )

    drivers_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution(
            [FindPackageShare('my_robot_bringup'), 'launch', 'drivers.launch.py']
        )), launch_arguments={'use_sim': use_sim}.items(),
    )

    perception_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution(
            [FindPackageShare('my_robot_bringup'), 'launch', 'perception.launch.py']
        )), condition=IfCondition(enable_perception),
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim', default_value='false'),
        DeclareLaunchArgument('enable_perception', default_value='true'),
        hardware_launch, drivers_launch, perception_launch,
    ])
```

---

## 🔋 Watch Dog & Heartbeat Monitoring

### systemd Watchdog Integration

```python
#!/usr/bin/env python3
# watchdog_node.py - ROS2 node that integrates with systemd watchdog

import os, socket, time
import rclpy
from rclpy.node import Node

class WatchdogNode(Node):
    def __init__(self):
        super().__init__('watchdog_node')
        watchdog_usec = os.environ.get('WATCHDOG_USEC')
        if watchdog_usec:
            interval_sec = int(watchdog_usec) / 1_000_000 / 2.0
        else:
            interval_sec = 10.0
        self.notify_socket = os.environ.get('NOTIFY_SOCKET')
        self._sd_notify('READY=1')
        self.get_logger().info(f'Watchdog started, interval: {interval_sec}s')
        self.create_timer(interval_sec, self._watchdog_tick)

    def _watchdog_tick(self):
        if self.notify_socket:
            addr = self.notify_socket
            if addr[0] == '@': addr = '\0' + addr[1:]
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            try:
                sock.connect(addr)
                sock.sendall(b'WATCHDOG=1')
            finally:
                sock.close()

def main():
    rclpy.init()
    node = WatchdogNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### ROS2-Level Heartbeat Monitor

```python
# heartbeat_monitor.py - Monitors heartbeats and triggers safe stop
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue

class HeartbeatMonitor(Node):
    def __init__(self):
        super().__init__('heartbeat_monitor')
        self.declare_parameter('monitored_nodes', ['motor_controller', 'camera_driver'])
        self.last_heartbeat = {n: time.time() for n in self.get_parameter('monitored_nodes').value}
        self.get_logger().info(f'Monitoring: {self.last_heartbeat.keys()}')

    def _check_health(self):
        now = time.time()
        for node_name, last_time in self.last_heartbeat.items():
            elapsed = now - last_time
            if elapsed > 5.0:  # timeout
                self.get_logger().warning(f'Heartbeat timeout: {node_name}')
                self.publish_emergency_stop()

    def publish_emergency_stop(self):
        estop = Bool()
        estop.data = True
        self.estop_pub.publish(estop)

# ... full implementation in reference file
```

---

## 📁 udev Rules untuk Perangkat Stabil

### File: `/etc/udev/rules.d/99-robot-devices.rules`

```bash
# Camera - stable symlink based on USB path
SUBSYSTEM=="video4linux", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", \
  KERNELS=="1-1.2:1.0", SYMLINK+="robot/camera_front", MODE="0666", GROUP="video"

# LiDAR
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", \
  ATTRS{serial}=="0001", SYMLINK+="robot/lidar", MODE="0666", GROUP="dialout"

# IMU
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", \
  ATTRS{serial}=="AB0CDEFG", SYMLINK+="robot/imu", MODE="0666", GROUP="dialout"
```

**Reload rules:**
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

---

## 🔧 Log Rotation & Monitoring

### journald Configuration: `/etc/systemd/journald.conf.d/robot.conf`

```ini
[Journal]
Storage=persistent
SystemMaxUse=1G
SystemMaxFileSize=100M
MaxRetentionSec=30day
RateLimitIntervalSec=10s
RateLimitBurst=10000
ForwardToSyslog=yes
```

### logrotate config: `/etc/logrotate.d/ros2`

```bash
/var/log/ros2/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 robot robot
    maxsize 100M
    dateext
    postrotate
        systemctl kill --signal=HUP robot-bringup.service 2>/dev/null || true
    endscript
}
```

---

## 📌 Practical Checklist for Drone Bringup

- [ ] udev rules for semua USB device (kamera, LiDAR, serial)
- [ ] systemd service units untuk tiap layer (drivers, perception, application)
- [ ] ROS2 environment file di `/etc/robot/ros2.env`
- [ ] CycloneDDS XML dengan peer list untuk multi-machine discovery
- [ ] Launch files berlapis dengan conditional arguments (sim/real, variant)
- [ ] Health check scripts untuk `ExecStartPre`
- [ ] Watchdog integration (WatchdogSec + sd_notify)
- [ ] Heartbeat monitor node untuk deteksi kegagalan node
- [ ] Graceful shutdown handler (zero velocity, engage brakes)
- [ ] Log rotation via logrotate + journald
- [ ] Restart policies rate-limited
- [ ] Resource limits (MemoryMax, CPUQuota)
- [ ] Network & firewall (static IP, DDS port rules)
- [ ] Full boot test dari power-off sampai operasi autonomo

---

## 🚀 Deployment Script (Optional)

Lihat `references/deploy-to-drone.sh` untuk script deploy otomatis via SSH.

---

## 📌 Next Steps After Learning

✅ Memahami lapisan bringup (hardware → driver → perception → application)  
✅ Membuat systemd service unit template untuk drone Bos  
✅ Menyusun udev rules untuk perangkat drone  
✅ Mengimplementasikan watchdog & heartbeat monitor  
✅ Menguji seluruh stack via `systemctl start robot-bringup.target`  

---

*Observation logged by Task Observer protocol.*
