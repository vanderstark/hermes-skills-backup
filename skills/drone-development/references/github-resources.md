# Drone Development — Reference Guide

## Key Resources by Topic

### ROS 2 & Gazebo
- **ROS 2 Official Docs:** https://docs.ros.org/en/humble/
- **Gazebo Harmonic:** https://gazebosim.org/docs/harmonic/
- **ROS 2 DDS Middleware:** https://docs.ros.org/en/humble/Concepts/Intermediate/DDS-and-ROS-middleware.html

### Flight Control Stacks
- **PX4 Docs:** https://docs.px4.io/main/en/
- **ArduPilot Docs:** https://ardupilot.org/copter/
- **MAVLink Protocol:** https://mavlink.io/

### GitHub Repositories (Integrated)
1. **ROS 2 + ArduPilot + Gazebo**
   - URL: https://github.com/AbdullahArpaci/ros2-ardupilot-gazebo-harmonic-drone-simulation-tutorial
   - Best for: Multi-drone simulation learning
   - Commands:
     ```bash
     git clone https://github.com/AbdullahArpaci/ros2-ardupilot-gazebo-harmonic-drone-simulation-tutorial.git
     cd ros2-ardupilot-gazebo-harmonic-drone-simulation-tutorial
     colcon build
     ```

2. **PX4 ROS 2 Control (sverk-ros2)**
   - URL: https://github.com/last1162/sverk-ros2
   - Best for: Autonomous flight control with odometry
   - Launch:
     ```bash
     ros2 launch sverk_ros2 px4_controller.launch.py
     ```

3. **Advanced Control Theory**
   - URL: https://github.com/evannsmc/evannsmc
   - Best for: PhD-level flight controllers
   - Research-ready for real quadrotors

### Sensors & Hardware
- **Pixhawk Hardware:** https://docs.px4.io/main/en/flight_controller/pixhawk.html
- **IMU Calibration:** https://docs.px4.io/main/en/config/accelerometer.html
- **GPS Configuration:** https://docs.px4.io/main/en/gps_compass/

### Safety Standards
- **ANSI R1506 (Robotics Safety):** Industry standard
- **Airspace Regulations:** Check local aviation authority (FAA, EASA, etc.)
