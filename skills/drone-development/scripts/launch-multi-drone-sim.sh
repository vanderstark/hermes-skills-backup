#!/bin/bash
# launch-multi-drone-sim.sh — Launch multi-drone Gazebo simulation with ROS 2

source /opt/ros/humble/setup.bash
source ~/drone_ws/install/setup.bash

echo "🚁 Launching Multi-Drone Gazebo Simulation"
echo "=========================================="

# Start Gazebo with empty world
echo "🎮 Starting Gazebo..."
gazebo -s libgazebo_ros_factory.so ~/drone_ws/install/px4_gazebo/share/px4_gazebo/worlds/empty.world &

sleep 3

# Launch ROS 2 autonomous controller (Drone 1)
echo "🤖 Launching Autonomous Flight Controller (Drone 1)..."
ros2 launch drone_control autonomous_flight.launch.py &

sleep 2

# Launch MAVProxy for drone communication
echo "📡 Starting MAVProxy telemetry..."
mavproxy.py --master=/dev/ttyACM0 --baudrate 57600 --aircraft drone1 &

echo ""
echo "✅ Multi-drone simulation launched!"
echo ""
echo "📊 Monitor drone:"
echo "   - QGroundControl: http://localhost:8000"
echo "   - Terminal: ros2 node list"
echo "   - Gazebo: Drag drone in scene"
echo ""
echo "🛑 To stop: pkill -f gazebo; pkill -f ros2"
