# Student Guide - Applied Robotics Course

Welcome to the Applied Robotics course! This guide will help you submit your assignments correctly and learn professional robotics development practices.

## 🎯 Learning Objectives

This course teaches you:
- **Modern Robotics Development**: ROS2, simulation, and hardware integration
- **AI-Robotics Integration**: Applying AI concepts to physical robotic systems
- **Real-time Systems**: Developing responsive robotic control systems
- **Professional Workflow**: Real-world robotics development practices

## 🚀 Quick Start

### 1. Fork the Repository
1. Go to the main course repository on GitHub
2. Click the "Fork" button in the top right
3. This creates your own copy of the repository

### 2. Clone Your Fork
```bash
# Replace 'your-username' with your actual GitHub username
git clone https://github.com/your-username/applied-robotics-course.git
cd applied-robotics-course
```

### 3. Set Up Your Environment
```bash
# Install ROS2 Humble (Ubuntu 20.04/22.04)
sudo apt update
sudo apt install ros-humble-desktop

# Create a Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install course dependencies
pip install -r requirements.txt

# Source ROS2 environment
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 4. Hardware Setup (if available)
```bash
# For TurtleBot3 users
sudo apt install ros-humble-turtlebot3*
echo "export TURTLEBOT3_MODEL=burger" >> ~/.bashrc

# For simulation-only users
sudo apt install ros-humble-gazebo*
```

## 📁 Assignment Structure

### Your Submission Folder
Create your work in the `student-submissions/` folder:

```
student-submissions/
└── your-username/
    ├── week-01/
    │   ├── README.md
    │   ├── src/
    │   │   ├── robot_controller.py
    │   │   └── launch/
    │   ├── requirements.txt
    │   └── simulation/
    ├── week-02/
    │   ├── README.md
    │   ├── src/
    │   │   ├── ai_agent_controller.py
    │   │   └── config/
    │   ├── launch/
    │   └── results/
    └── ...
```

### Required Files for Each Week
- **README.md**: Project description and setup instructions
- **src/**: Source code for ROS2 nodes and Python scripts
- **launch/**: ROS2 launch files for running your robot
- **requirements.txt**: Python packages used
- **simulation/**: Gazebo worlds or simulation files (if applicable)
- **results/**: Videos, images, or data from robot experiments

## 📝 Working on Assignments

### Step 1: Create Your Week Folder
```bash
# Create your week folder
mkdir -p student-submissions/your-username/week-01

# Navigate to your assignment folder
cd student-submissions/your-username/week-01
```

### Step 2: Set Up ROS2 Workspace
```bash
# Create ROS2 workspace structure
mkdir -p src
mkdir -p launch
mkdir -p config

# Create your ROS2 package
cd src
ros2 pkg create --build-type ament_python your_robot_package --dependencies rclpy std_msgs geometry_msgs
```

### Step 3: Develop Your Solution
- Write your robot control code in `src/`
- Create launch files for easy robot startup
- Test in simulation first, then on hardware
- Document your approach and results

### Step 4: Test Your Robot
```bash
# Build your workspace
cd student-submissions/your-username/week-01
colcon build

# Source the setup
source install/setup.bash

# Launch your robot
ros2 launch your_robot_package robot_launch.py
```

## 🚀 Submission Process

### Step 1: Prepare Your Submission
```bash
# Make sure all files are in place
ls student-submissions/your-username/week-01/
# Should show: README.md, src/, launch/, requirements.txt, etc.

# Test your robot one final time
ros2 launch your_robot_package robot_launch.py
```

### Step 2: Create Documentation
Your `README.md` should include:
- **Robot Description**: What your robot does
- **Setup Instructions**: How to build and run your code
- **Dependencies**: ROS2 packages and Python libraries needed
- **Usage**: Commands to launch and test your robot
- **Results**: Videos, images, or data from testing
- **Challenges**: Problems encountered and solutions
- **AI Integration**: How you applied AI course concepts

### Step 3: Record Demonstration
```bash
# Record your robot in action
ros2 bag record /cmd_vel /scan /camera/image_raw -o robot_demo

# Or record screen/video of simulation
# Save as: results/robot_demo.mp4
```

### Step 4: Commit and Push
```bash
# Add your changes
git add student-submissions/your-username/week-01/

# Commit with descriptive message
git commit -m "Week 1: Robot controller with basic navigation"

# Push to your fork
git push origin main
```

### Step 5: Create Pull Request
1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Title: "Week 1 Submission - Your Name"
4. Description: Brief summary of your robot implementation
5. Submit the pull request

## 📋 Submission Checklist

Before submitting, verify:
- [ ] All code is in the correct folder structure
- [ ] ROS2 workspace builds successfully with `colcon build`
- [ ] Robot launches without errors
- [ ] README.md is comprehensive and clear
- [ ] Dependencies are listed in requirements.txt
- [ ] Results include video or demonstration
- [ ] Code follows ROS2 and Python style guidelines
- [ ] No sensitive information (API keys, passwords)
- [ ] All files are in the correct folder structure

### Code Quality Standards
- **Clean Code**: Use clear variable names and comments
- **ROS2 Best Practices**: Follow ROS2 coding conventions
- **Error Handling**: Handle potential robot errors gracefully
- **Documentation**: Include docstrings for functions and classes
- **Testing**: Test robot behavior in different scenarios

## 🎯 Example Submission

### Week 1: Robot Setup and Basic Control

**File Structure:**
```
student-submissions/john-doe/week-01/
├── README.md
├── src/
│   └── basic_robot_controller/
│       ├── __init__.py
│       ├── robot_controller.py
│       └── setup.py
├── launch/
│   └── robot_launch.py
├── requirements.txt
├── config/
│   └── robot_params.yaml
└── results/
    ├── robot_demo.mp4
    └── navigation_test.bag
```

**README.md Example:**
```markdown
# Week 1: Basic Robot Controller

## Description
This assignment implements a basic robot controller that moves the robot in a square pattern while avoiding obstacles.

## Setup Instructions
1. Build the workspace: `colcon build`
2. Source the setup: `source install/setup.bash`
3. Launch the robot: `ros2 launch robot_launch.py`

## Features
- Basic robot movement control
- Obstacle avoidance using laser scanner
- ROS2 parameter configuration
- Simulation and hardware compatibility

## AI Integration
- Applied environment setup knowledge from AI course
- Used structured programming practices from AI development

## Dependencies
- ROS2 Humble
- Python 3.8+
- Gazebo for simulation
- TurtleBot3 packages

## Usage
```bash
# Launch in simulation
ros2 launch robot_launch.py use_sim_time:=true

# Launch with real robot
ros2 launch robot_launch.py use_sim_time:=false
```

## Results
- Successfully navigated square pattern
- Avoided obstacles in simulation
- Recorded demonstration in results/robot_demo.mp4

## Challenges
- Tuning PID parameters for smooth movement
- Handling laser scanner data filtering
- Synchronizing simulation and real robot behavior

## Learning Outcomes
- Learned ROS2 node structure and communication
- Understood robot coordinate systems
- Gained experience with robot simulation
```

## ❌ Common Mistakes to Avoid

### Don't Do This
- Submit work outside the `student-submissions/` folder
- Forget to include launch files or package dependencies
- Submit code that doesn't build with `colcon build`
- Include large bag files without compression
- Forget to test robot behavior before submission
- Use absolute paths in launch files

### ✅ Do This Instead
- Put all work in `student-submissions/your-username/week-X/`
- Include all necessary ROS2 packages and launch files
- Test robot builds and runs successfully
- Compress large files or use external storage links
- Document robot behavior with videos/images
- Use relative paths and ROS2 parameters

## 🤖 Robotics-Specific Guidelines

### Hardware Safety
- Always use emergency stop when testing with real robots
- Follow lab safety protocols
- Never leave robots running unattended
- Check battery levels before extended testing

### Simulation Best Practices
- Test in simulation before real robot deployment
- Use appropriate Gazebo worlds for testing
- Verify sensor data is realistic
- Document simulation vs. real robot differences

### ROS2 Development
- Follow ROS2 naming conventions
- Use launch files for complex robot systems
- Implement proper error handling for robot failures
- Use ROS2 parameters for robot configuration

## 🔄 AI Course Integration

### Shared Skills
- **Python Development**: Common programming practices
- **Git Workflow**: Same version control process
- **Testing**: Automated testing for robot code
- **Documentation**: Clear project documentation

### Applied AI Concepts
- **Week 1**: Apply AI environment setup to robotics
- **Week 2**: Use AI agents for robot decision making
- **Week 3**: Apply fine-tuned models to robot perception
- **Week 4**: Implement multimodal AI in robots
- **Week 5**: Create robot APIs using AI knowledge
- **Week 6**: Build robot interfaces with frontend skills
- **Week 7**: Apply CI/CD to robot deployment
- **Week 8**: Integrate AI and robotics in capstone project

## 📞 Support Resources

### Technical Support
- **Discord**: `#robotics-support` for general questions
- **Hardware Help**: `#hardware-troubleshooting` for robot issues
- **Office Hours**: Monday & Wednesday 2-4 PM
- **Lab Access**: Sign up for hands-on robot testing

### Learning Resources
- **ROS2 Documentation**: Official tutorials and guides
- **Simulation Environments**: Pre-configured Gazebo worlds
- **Hardware Guides**: Robot setup and troubleshooting
- **Video Tutorials**: Step-by-step robot development

### Community
- **Study Groups**: Collaborate on robotics projects
- **Robotics Club**: Extended learning opportunities
- **Peer Review**: Get feedback on robot implementations
- **Cross-course Collaboration**: Work with AI course students

## 🏆 Success Tips

- **Start Early**: Robotics can be unpredictable, allow extra time
- **Test Frequently**: Continuous testing prevents major issues
- **Document Everything**: Keep detailed notes on robot behavior
- **Ask for Help**: Don't struggle alone with robot problems
- **Safety First**: Always prioritize safety in robot testing
- **Learn from Failures**: Robot failures are learning opportunities

---

**This course combines hands-on robotics experience with AI knowledge from the parallel course. Students will develop both technical skills and practical experience needed for professional robotics development.** 