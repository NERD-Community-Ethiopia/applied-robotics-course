# Contributing to Applied Robotics Course

Thank you for your interest in contributing to this course! This document provides comprehensive guidelines for students, contributors, and administrators.

## 🚀 Quick Links

- **[Intern Guide](INTERN_GUIDE.md)** - For interns working on course development
- **[Student Guide](STUDENT_GUIDE.md)** - For students submitting assignments
- **[Security Policy](security.md)** - Security guidelines and reporting
- **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community guidelines

## 🏗️ Project Structure

```
applied-robotics-course/
├── .github/                    # GitHub configuration
│   ├── workflows/             # CI/CD pipelines
│   ├── ISSUE_TEMPLATE/        # Issue templates
│   └── pull_request_template.md
├── lectures/                  # Course lecture materials
├── workshops/                 # Hands-on workshop materials
├── student-submissions/       # Student assignment submissions
├── scripts/                   # Automation and utility scripts
├── tests/                     # Test suite
├── docs/                      # Documentation
└── capstone-projects/         # Final projects
```

## 🎓 For Students

**Please see [STUDENT_GUIDE.md](STUDENT_GUIDE.md) for detailed submission instructions.**

### Quick Overview

- Fork the repository
- Work in `student-submissions/your-username/week-X/`
- Submit PRs from your fork's main branch
- No feature branches needed

### Learning Objectives

- Build and program autonomous robots
- Integrate AI models with robotic systems
- Work with sensors, actuators, and embedded systems
- Develop real-time robotic applications
- Deploy robotics solutions using modern DevOps practices
- Learn modern development practices: CI/CD, testing, security, collaboration

## 🤝 For Contributors

- Create a feature branch from `develop` or your personal branch
- Write clear, concise commit messages
- Ensure your code passes all tests and lint checks
- Submit a pull request with a detailed description

## 🧪 Code Quality

- Use Black for formatting, Flake8 for linting, and MyPy for type checking
- Run `make lint` and `make test` before submitting
- Add or update tests for new features or bug fixes

## 🛡️ Security

- Do not submit sensitive information or credentials
- Report security issues via [security.md](security.md)

## 🌐 Community

- Be respectful and follow our [Code of Conduct](CODE_OF_CONDUCT.md)
