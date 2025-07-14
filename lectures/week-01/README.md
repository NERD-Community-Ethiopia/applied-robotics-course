# Week 1: Introduction to Robotics & ROS Setup

## 📚 Lecture Overview

Welcome to the Applied Robotics course! This week we'll introduce you to the fundamentals of robotics and set up your ROS2 development environment. This course runs in parallel with the Generative AI & Automation course, allowing you to apply AI concepts to real-world robotic systems.

## 🎯 Learning Objectives

By the end of this week, you will:
- Understand the fundamentals of robotics and autonomous systems
- Set up your ROS2 development environment
- Create your first robot node and controller
- Understand how robotics integrates with AI systems
- Learn the course workflow and submission process

## 📖 Lecture Content

### 1. Introduction to Robotics

**What is Robotics?**
- Definition: The intersection of mechanical engineering, electrical engineering, and computer science
- Autonomous systems that can perceive, reason, and act in the physical world
- Applications: Manufacturing, healthcare, transportation, exploration, service robots

**Key Components of Robotic Systems:**
- **Sensors**: Cameras, LiDAR, IMU, encoders, force sensors
- **Actuators**: Motors, servos, grippers, wheels
- **Computing**: Microcontrollers, single-board computers, edge AI
- **Software**: Control algorithms, perception, planning, AI integration

**Types of Robots:**
- Industrial robots (manufacturing)
- Service robots (healthcare, cleaning)
- Mobile robots (autonomous vehicles, drones)
- Humanoid robots (social interaction)
- Exploration robots (space, underwater)

### 2. Robot Operating System (ROS2)

**What is ROS2?**
- Open-source middleware for robot software development
- Provides tools, libraries, and conventions for building robot applications
- Successor to ROS1 with improved real-time performance and security

**Core ROS2 Concepts:**
- **Nodes**: Independent processes that perform specific tasks
- **Topics**: Communication channels for data exchange
- **Services**: Request-response communication
- **Actions**: Long-running tasks with feedback
- **Parameters**: Configuration settings for nodes

**ROS2 Architecture:**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Sensor    │    │   Control   │    │  Actuator   │
│    Node     │───▶│    Node     │───▶│    Node     │
└─────────────┘    └─────────────┘    └─────────────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │
                    ┌─────────────┐
                    │   AI Agent  │
                    │    Node     │
                    └─────────────┘
```

### 3. Development Environment Setup

**Required Software:**
- **Ubuntu 20.04 LTS** (recommended) or 22.04 LTS
- **ROS2 Humble Hawksbill** (latest LTS release)
- **Python 3.8+** for robot programming
- **Gazebo** for robot simulation
- **VS Code** with ROS extensions

**Installation Steps:**
```bash
# Update system
sudo apt update && sudo apt upgrade

# Install ROS2 Humble
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt install ros-humble-desktop

# Install development tools
sudo apt install python3-colcon-common-extensions
sudo apt install python3-rosdep2
sudo rosdep init
rosdep update
```

### 4. First Robot Application

**Creating Your First Node:**
```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class BasicRobotController(Node):
    def __init__(self):
        super().__init__('basic_robot_controller')
        
        # Publisher for robot movement
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Subscriber for sensor data
        self.sensor_sub = self.create_subscription(
            String, '/sensor_data', self.sensor_callback, 10)
        
        # Timer for periodic control
        self.timer = self.create_timer(0.1, self.control_loop)
        
        self.get_logger().info('Robot controller started')
    
    def sensor_callback(self, msg):
        """Process sensor data"""
        self.get_logger().info(f'Sensor data: {msg.data}')
    
    def control_loop(self):
        """Main control loop"""
        twist = Twist()
        twist.linear.x = 0.5  # Move forward
        twist.angular.z = 0.0  # No rotation
        
        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    controller = BasicRobotController()
    
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Launch File Example:**
```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='basic_robot_controller',
            executable='robot_controller',
            name='basic_robot_controller',
            output='screen',
            parameters=[
                {'robot_name': 'my_robot'},
                {'max_speed': 1.0}
            ]
        )
    ])
```

### 5. Integration with AI Course

**Shared Technologies:**
- **Python**: Common programming language for both courses
- **Git/GitHub**: Version control and collaboration
- **Docker**: Containerization for deployment
- **CI/CD**: Automated testing and deployment
- **APIs**: Communication between AI and robot systems

**AI-Robotics Integration Points:**
- **Perception**: Use computer vision models for robot vision
- **Decision Making**: Apply AI agents for robot behavior
- **Natural Language**: Enable voice commands and interaction
- **Learning**: Adapt robot behavior based on experience
- **Planning**: Use AI for path planning and task scheduling

**Example AI-Robot Integration:**
```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import cv2
from cv_bridge import CvBridge
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

class AIRobotController(Node):
    def __init__(self):
        super().__init__('ai_robot_controller')
        
        # Initialize AI agent (from AI course)
        self.ai_agent = initialize_agent(
            llm=OpenAI(api_key="your_key"),
            tools=[],
            agent_type="zero-shot-react-description"
        )
        
        # ROS2 interfaces
        self.image_sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.bridge = CvBridge()
    
    def image_callback(self, msg):
        """Process camera image with AI"""
        # Convert ROS image to OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        
        # Process with AI (example: object detection)
        result = self.ai_agent.run(
            f"Analyze this image and decide robot movement: {cv_image.shape}"
        )
        
        # Convert AI decision to robot command
        twist = Twist()
        if "move forward" in result.lower():
            twist.linear.x = 0.5
        elif "turn left" in result.lower():
            twist.angular.z = 0.5
        elif "turn right" in result.lower():
            twist.angular.z = -0.5
        
        self.cmd_pub.publish(twist)
```

## 🛠️ Workshop Preparation

**Pre-workshop Tasks:**
1. Complete ROS2 installation
2. Set up development environment
3. Test basic ROS2 commands
4. Familiarize yourself with the course repository

**Workshop Goals:**
- Set up ROS2 workspace
- Create your first robot package
- Implement basic robot control
- Test in simulation environment
- Understand ROS2 debugging tools

**Required Hardware (if available):**
- TurtleBot3 Burger or equivalent
- Laptop with Ubuntu 20.04/22.04
- USB cable for robot connection
- Sufficient workspace for robot testing

## 📚 Additional Resources

**Reading Materials:**
- [ROS2 Documentation](https://docs.ros.org/en/humble/) - Official ROS2 tutorials
- [Introduction to Robotics](https://www.amazon.com/Introduction-Robotics-Mechanics-Planning-Control/dp/0133489795) - Craig textbook
- [Modern Robotics](http://hades.mech.northwestern.edu/index.php/Modern_Robotics) - Lynch & Park
- [Robotics: Vision and Control](https://petercorke.com/rvc/) - Peter Corke

**Videos:**
- [ROS2 Basics](https://www.youtube.com/watch?v=bJB9tv4ThV4)
- [Robot Operating System Explained](https://www.youtube.com/watch?v=7TNjuKYWbIk)
- [TurtleBot3 Tutorial](https://www.youtube.com/watch?v=1tqg_GqZxNM)

**Tools & Platforms:**
- [ROS2 Humble Documentation](https://docs.ros.org/en/humble/)
- [Gazebo Robot Simulation](https://gazebosim.org/)
- [TurtleBot3 Manual](https://emanual.robotis.com/docs/en/platform/turtlebot3/)
- [OpenCV Documentation](https://opencv.org/)

## 📝 Assignment

**Due Date**: End of Week 2

**Tasks:**
1. Set up complete ROS2 development environment
2. Create a basic robot controller package
3. Implement simple robot behaviors (move forward, turn, stop)
4. Test your controller in Gazebo simulation
5. Document your setup process and results

**Deliverables:**
- ROS2 package with robot controller
- Launch files for easy robot startup
- Documentation of setup and usage
- Video demonstration of robot behavior
- Integration plan with AI course concepts

**Submission Structure:**
```
student-submissions/your-username/week-01/
├── README.md
├── src/
│   └── basic_robot_controller/
│       ├── __init__.py
│       ├── robot_controller.py
│       └── setup.py
├── launch/
│   └── robot_launch.py
├── config/
│   └── robot_params.yaml
├── requirements.txt
└── results/
    ├── robot_demo.mp4
    └── setup_screenshots/
```

## 🎯 Next Week Preview

**Week 2: Robot Control & AI Agent Integration**
- Advanced robot kinematics and control
- Integrating AI agents with robot decision-making
- Sensor fusion and perception basics
- Using LangChain agents for robot behavior

## 💡 Tips for Success

### Technical Tips
- **Start with Simulation**: Test everything in Gazebo before real hardware
- **Use ROS2 Tools**: Learn `ros2 topic`, `ros2 service`, `ros2 node` commands
- **Debug Systematically**: Use `ros2 topic echo` to monitor data flow
- **Document Everything**: Keep detailed notes on robot behavior

### Safety Tips
- **Emergency Stop**: Always have a way to stop the robot quickly
- **Test Area**: Ensure adequate space for robot movement
- **Battery Management**: Monitor battery levels during testing
- **Gradual Testing**: Start with slow movements, increase speed gradually

### Integration Tips
- **Connect with AI Course**: Apply AI concepts to robot problems
- **Share Knowledge**: Collaborate with AI course students
- **Think Practically**: Consider real-world robot constraints
- **Iterate Quickly**: Test, learn, and improve continuously

## 📞 Support

- **Discord Support**: `#robotics-support`
- **Hardware Help**: `#hardware-troubleshooting`
- **Office Hours**: Monday & Wednesday 2-4 PM
- **Lab Access**: Sign up for hands-on robot testing time
- **Cross-course Support**: `#ai-robotics-integration`

## 🚀 Looking Ahead

This week establishes the foundation for the entire course. You'll build upon these concepts to create increasingly sophisticated robot systems that integrate with AI capabilities. The combination of robotics and AI will prepare you for cutting-edge applications in autonomous systems, industrial automation, and service robotics.

---

**Remember: This course is designed to complement your AI learning. Every concept you learn in the AI course can be applied to make robots more intelligent and capable!** 