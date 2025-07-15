# Intern Guide - Applied Robotics Course

Welcome to the team! This guide will help you contribute effectively to the Applied Robotics Course project and learn professional development practices.

## 🎯 Learning Objectives

As an intern, you'll learn:

- **Professional Development**: Real-world software development practices
- **CI/CD Pipelines**: Automated testing, building, and deployment
- **Code Quality**: Linting, testing, and security best practices
- **Collaboration**: Working in teams with Git and GitHub
- **Project Management**: Agile development and task management

## 🚀 Quick Start

### 1. Initial Setup

```bash
# Clone the repository with SSH
git clone git@github.com/NERD-Community-Ethiopia/applied-robotics-course.git
cd applied-robotics-course

# Configure Git for DCO sign-off
git config --global format.signoff true
git config --global user.name "Your Full Name"
git config --global user.email "your-email@example.com"

# Create your personal branch
git checkout -b intern/your-name
git push -u origin intern/your-name

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"
```
