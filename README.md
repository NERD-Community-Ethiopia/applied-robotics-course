# Applied Robotics – Course Repository

Welcome to the official repository for the **Applied Robotics** course. This project demonstrates modern robotics development practices including hardware integration, simulation, real-time systems, and AI-powered robotic applications.

## 🚀 Quick Links

- **[Student Guide](STUDENT_GUIDE.md)** - How to submit assignments
- **[Intern Guide](INTERN_GUIDE.md)** - Development workflow for team members
- **[Contributing Guidelines](CONTRIBUTING.md)** - Complete contribution guide
- **[Security Policy](security.md)** - Security guidelines and reporting
- **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community guidelines

## 📚 Course Overview

This is an 8-week intensive course for intermediate/advanced students to gain hands-on experience with:
- Building and programming autonomous robots
- Integrating AI models with robotic systems
- Working with sensors, actuators, and embedded systems
- Developing real-time robotic applications
- Deploying robotics solutions using modern DevOps practices
- **Modern Development Practices**: CI/CD, testing, security, collaboration

**This course runs in parallel with the Generative AI & Automation course**, allowing students to apply their AI knowledge to real-world robotic applications.

Each week includes 3 hours of lectures and 3 hours of practical workshops.

## 🏗️ Repository Structure

```
applied-robotics-course/
├── .github/                    # GitHub configuration
│   ├── workflows/             # CI/CD pipelines
│   ├── ISSUE_TEMPLATE/        # Issue templates
│   └── pull_request_template.md
├── lectures/week-01/          # Weekly lecture materials
├── workshops/week-01/         # Workshop starter kits
├── student-submissions/       # Student assignment submissions
├── scripts/                   # Automation and utility scripts
├── tests/                     # Test suite
├── docs/                      # Documentation
├── capstone-projects/         # Final projects
├── simulations/              # Robot simulation environments
├── hardware/                 # Hardware setup guides
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Modern Python configuration
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Local development setup
├── Makefile                 # Development commands
└── README.md                # This file
```

## 🔄 CI/CD Pipeline

This project implements a comprehensive CI/CD pipeline that demonstrates real-world robotics development practices:

### Pipeline Stages
1. **Quality Check**: Linting, formatting, type checking
2. **Testing**: Unit tests, integration tests, simulation tests
3. **Security**: Vulnerability scanning and safety checks
4. **Hardware Validation**: Automated hardware compatibility checks
5. **Simulation**: Robot behavior validation in virtual environments
6. **Deploy**: Staging and production deployment to robotic systems

### Branch Strategy
- **`main`**: Production-ready code (admin only)
- **`develop`**: Integration branch for contributors
- **`intern/*`**: Personal branches for interns
- **`feature/*`**: Feature development branches
- **`hotfix/*`**: Emergency fixes

### Automated Checks
- ✅ Code formatting (Black)
- ✅ Style checking (Flake8)
- ✅ Type checking (MyPy)
- ✅ Security scanning (Bandit, Safety)
- ✅ Test coverage (Pytest)
- ✅ Hardware compatibility tests
- ✅ Simulation validation
- ✅ Student submission validation

## 🚀 Getting Started

### For Students
1. **Fork** this repository to your GitHub account
2. **Clone** your fork locally
3. **Work** in `student-submissions/your-username/week-X/`
4. **Submit** via Pull Request from your fork's main branch

### For Contributors/Interns
1. **Clone** the repository
2. **Create** your personal branch: `intern/your-name`
3. **Install** dependencies: `make install`
4. **Start** development: `make setup`

### For Administrators
1. **Review** PRs to develop branch
2. **Test** develop branch thoroughly
3. **Merge** to main when ready
4. **Deploy** to production systems

## 🛠️ Hardware Requirements

### Basic Setup
- **Single Board Computer**: Raspberry Pi 4 or NVIDIA Jetson Nano
- **Sensors**: Camera, LiDAR, IMU, ultrasonic sensors
- **Actuators**: Servo motors, stepper motors, DC motors
- **Development Board**: Arduino or equivalent
- **Connectivity**: WiFi, Bluetooth modules

### Advanced Setup
- **Robot Platform**: TurtleBot3, ROSbot, or custom chassis
- **Manipulator**: Robotic arm (optional)
- **Advanced Sensors**: Depth cameras, force sensors
- **Computing**: NVIDIA Jetson Xavier or Intel NUC

### Software Requirements
- **Operating System**: Ubuntu 20.04 LTS
- **ROS**: Robot Operating System (ROS2 Humble)
- **Simulation**: Gazebo, Webots, or CoppeliaSim
- **AI Integration**: Python, PyTorch, TensorFlow
- **Development**: Docker, Git, VS Code

## 🎯 Course Integration with AI Bootcamp

This robotics course is designed to complement the parallel Generative AI & Automation course:

### Week-by-Week Integration
- **Week 1**: Apply AI setup knowledge to robotics environments
- **Week 2**: Use AI agents for robot control and decision-making
- **Week 3**: Implement fine-tuned models for robot perception
- **Week 4**: Build multimodal robotic systems (vision + language)
- **Week 5**: Deploy robot APIs and services
- **Week 6**: Create robot user interfaces and HMI
- **Week 7**: Automate robot deployment and testing
- **Week 8**: Integrated AI-Robotics capstone project

### Shared Technologies
- **Python**: Common programming language
- **Docker**: Containerization for both AI and robot applications
- **CI/CD**: Same development practices
- **Git**: Version control for all projects
- **APIs**: RESTful services for robot-AI communication

## 📅 Course Schedule

- **Week 1**: Introduction to Robotics & ROS Setup
- **Week 2**: Robot Control & AI Agent Integration
- **Week 3**: Sensor Integration & Perception
- **Week 4**: Computer Vision & Multimodal Robotics
- **Week 5**: Robot Navigation & Path Planning
- **Week 6**: Human-Robot Interaction & Interfaces
- **Week 7**: Robot Deployment & Fleet Management
- **Week 8**: Integrated AI-Robotics Capstone Project

## 🛠️ Tech Stack

### Robotics & Hardware
- **ROS2**: Robot Operating System
- **Gazebo**: Robot simulation
- **OpenCV**: Computer vision
- **PCL**: Point cloud processing
- **MoveIt**: Motion planning
- **Navigation2**: Robot navigation

### AI Integration
- **PyTorch**: Deep learning framework
- **OpenAI**: API integration for robot reasoning
- **LangChain**: AI application framework for robots
- **Transformers**: Hugging Face library
- **YOLO**: Object detection
- **MediaPipe**: Pose estimation

### Development & DevOps
- **Git & GitHub**: Version control and collaboration
- **Docker**: Containerization
- **GitHub Actions**: CI/CD pipelines
- **Pytest**: Testing framework
- **Black**: Code formatting
- **MyPy**: Type checking

### Deployment & Monitoring
- **Kubernetes**: Container orchestration
- **Prometheus**: Monitoring
- **Grafana**: Visualization
- **ROS2 Bag**: Data logging
- **Foxglove**: Robot data visualization

## 🔒 Safety & Security

### Safety Protocols
- **Emergency Stop**: All robots must have emergency stop functionality
- **Safety Boundaries**: Virtual and physical safety zones
- **Risk Assessment**: Comprehensive safety evaluation
- **Hardware Validation**: Continuous hardware health monitoring

### Security Measures
- **Secure Communication**: Encrypted robot-to-robot communication
- **Access Control**: Role-based access to robot systems
- **Vulnerability Scanning**: Regular security audits
- **Safe Deployment**: Staged rollout of robot software updates

## 🎯 Learning Objectives

By the end of this course, students will be able to:
- Design and build autonomous robotic systems
- Integrate AI models with real-world robotic applications
- Develop real-time robotic control systems
- Implement sensor fusion and perception algorithms
- Deploy and maintain robotic systems in production
- **Apply AI knowledge to solve real-world robotics challenges**
- **Use professional development tools and practices**
- **Collaborate effectively using Git and GitHub**
- **Write secure, tested, and maintainable robotics code**

## 🤝 Collaboration with AI Course

Students enrolled in both courses will:
- **Share Knowledge**: Apply AI concepts to robotics challenges
- **Joint Projects**: Collaborate on AI-robotics integration projects
- **Cross-Pollination**: Learn from both domains simultaneously
- **Practical Application**: See AI theory applied to physical systems
- **Enhanced Skills**: Develop full-stack AI-robotics capabilities

## 🏆 Career Outcomes

Graduates will be prepared for roles in:
- **Robotics Engineering**: Design and develop robotic systems
- **AI Robotics**: Integrate AI with robotic applications
- **Autonomous Systems**: Self-driving cars, drones, automation
- **Industrial Automation**: Manufacturing and process automation
- **Service Robotics**: Healthcare, hospitality, and service robots
- **Research & Development**: Academic and industrial research

## 📞 Support

- **Discord Server**: `#robotics-support`
- **Office Hours**: Mondays & Wednesdays 2-4 PM
- **Email**: robotics-instructor@nerd-ethiopia.org
- **Hardware Support**: `#hardware-help`

## 🌟 Prerequisites

- Basic programming knowledge (Python preferred)
- Understanding of linear algebra and calculus
- Familiarity with Linux/Ubuntu
- **Concurrent enrollment in Generative AI & Automation course recommended**

---

**This course teaches both robotics engineering and AI integration skills. Students learn to work like real robotics engineers while building cutting-edge AI-powered robotic systems.** 