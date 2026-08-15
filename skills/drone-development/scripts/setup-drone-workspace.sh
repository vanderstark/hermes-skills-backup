#!/bin/bash
# setup-drone-workspace.sh — Setup complete ROS 2 + PX4 + Gazebo drone development environment

set -e

echo "🚁 Drone Development Environment Setup"
echo "======================================="

# 1. Install ROS 2 Humble
echo "📦 Installing ROS 2 Humble..."
curl https://repo.ros2.org/ros.key | sudo apt-key add -
sudo sh -c 'echo "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'
sudo apt update
sudo apt install -y ros-humble-desktop ros-humble-gazebo-ros

# 2. Install Gazebo Harmonic
echo "📦 Installing Gazebo Harmonic..."
sudo apt install -y gazebo

# 3. Install Python & build tools
echo "📦 Installing colcon & development tools..."
sudo apt install -y python3-colcon-common-extensions python3-rosdep python3-pip

# 4. Create drone workspace
echo "🏗️  Creating ROS 2 drone workspace..."
mkdir -p ~/drone_ws/src
cd ~/drone_ws

# 5. Clone drone repositories
echo "🔄 Cloning drone GitHub repositories..."
cd src

echo "   → Cloning ROS 2 + ArduPilot + Gazebo tutorial..."
git clone https://github.com/AbdullahArpaci/ros2-ardupilot-gazebo-harmonic-drone-simulation-tutorial.git

echo "   → Cloning PX4 ROS 2 control stack..."
git clone https://github.com/last1162/sverk-ros2.git

echo "   → Cloning PX4-Autopilot firmware..."
git clone https://github.com/PX4/PX4-Autopilot.git
cd PX4-Autopilot
make distclean

# 6. Build workspace
echo "🔨 Building ROS 2 workspace..."
cd ~/drone_ws
colcon build --symlink-install

# 7. Install additional ROS 2 packages
echo "📦 Installing additional ROS 2 packages..."
sudo apt install -y \
    ros-humble-tf2 \
    ros-humble-tf2-tools \
    ros-humble-geometry-msgs \
    ros-humble-sensor-msgs \
    ros-humble-nav-msgs \
    ros-humble-mavros \
    ros-humble-mavros-extras

# 8. Setup environment
echo "✅ Setting up environment..."
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "source ~/drone_ws/install/setup.bash" >> ~/.bashrc

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Next steps:"
echo "   1. source ~/.bashrc"
echo "   2. cd ~/drone_ws"
echo "   3. gazebo &"
echo "   4. ros2 launch ... (launch files from cloned repos)"
echo ""
echo "📚 Documentation:"
echo "   - ROS 2: https://docs.ros.org/en/humble/"
echo "   - PX4: https://docs.px4.io/"
echo "   - Gazebo: https://gazebosim.org/docs/harmonic/"
