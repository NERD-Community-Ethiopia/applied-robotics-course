#!/usr/bin/env python3
"""
Automated Task Generation Script

This script generates GitHub issues for weekly tasks based on the course structure.
It creates tasks for lectures, workshops, assignments, and documentation.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

try:
    from github import Github, GithubException
except ImportError:
    print("Error: PyGithub not installed. Run: pip install PyGithub")
    sys.exit(1)


class TaskGenerator:
    def __init__(self, token: str, repo_name: str = "NERD-Community-Ethiopia/generative-ai-course"):
        self.github = Github(token)
        self.repo = self.github.get_repo(repo_name)
        self.week_templates = self._load_week_templates()
    
    def _load_week_templates(self) -> Dict:
        """Load task templates for each week"""
        return {
            "0": {
                "title": "Week 0 Onboarding & GitHub Workflow",
                "tasks": [
                    {
                        "title": "Set Up Your Dev Environment & Join Course Channels",
                        "body": (
                            "1. Install the required tools on your machine:\n"
                            "   - Python 3.8+, Git, Docker, VS Code\n"
                            "   - Follow the step-by-step guide (written or video) on Proton Drive.\n"
                            "2. Create accounts (if you don’t have them):\n"
                            "   - GitHub (github.com/signup)\n"
                            "   - Element (for Matrix chat)\n"
                            "   - Proton Drive (for resources)\n"
                            "3. Join our course rooms on Element and verify you can post.\n\n"
                            "**Deliverables:**\n"
                            "- Screenshot of terminal showing `python --version`, `git --version` and `docker --version`.\n"
                            "- Proof of joined course Element channel (a screenshot of your profile in the channel)."
                        ),
                        "labels": ["setup", "environment", "high-priority"],
                        "assignees": [],
                        "milestone": "Week 0 Onboarding"
                    },
                    {
                        "title": "Introduction to Version Control with Git & GitHub",
                        "body": (
                            "Watch/attend the 60-minute recorded/live lecture covering:\n"
                            "- What is version control and why it matters\n"
                            "- Core Git commands: `git init`, `git add`, `git commit`, `git status`, `git log`\n"
                            "- What is GitHub and collaborative workflows: forking, cloning, branching, pushing, pull requests\n"
                            "- How to label issues and PRs effectively\n\n"
                            "**Deliverables:**\n"
                            "- Complete a short quiz on Git basics (posted in Element).\n"
                            "- React to the lecture post with one question or insight."
                        ),
                        "labels": ["lecture", "git", "high-priority"],
                        "assignees": [],
                        "milestone": "Git & GitHub Workflow"
                    },
                    {
                        "title": "Hands-On: Forking and Cloning a Repository",
                        "body": (
                            "Step-by-step exercise:\n"
                            "1. Fork the starter repository on GitHub.\n"
                            "2. Clone your fork locally.\n"
                            "3. Verify your local setup by listing files and running a provided health-check script.\n\n"
                            "**Deliverables:**\n"
                            "- Post in Element with the URL of your fork and a screenshot of the health-check passing."
                        ),
                        "labels": ["workshop", "git", "high-priority"],
                        "assignees": [],
                        "milestone": "Git & GitHub Workflow"
                    },
                    {
                        "title": "Hands-On: Branching and Making Changes",
                        "body": (
                            "Guide to:\n"
                            "1. Create a new branch on your local repo:\n"
                            "   - `git checkout -b week0-<your-name>`\n"
                            "2. Make a simple code change (e.g., add `print(\"Hello, <Your Name>!\")` to `week0_<your-name>.py`).\n"
                            "3. Commit with a meaningful message:\n"
                            "   - `git add .`\n"
                            "   - `git commit -m \"feat: add hello script for <Your Name>\"`\n\n"
                            "**Deliverables:**\n"
                            "- A screenshot of your local branch list (`git branch`) and commit history (`git log -1`)."
                        ),
                        "labels": ["workshop", "git", "high-priority"],
                        "assignees": [],
                        "milestone": "Git & GitHub Workflow"
                    },
                    {
                        "title": "Hands-On: Pushing Changes & Creating a Pull Request",
                        "body": (
                            "1. Push your branch to GitHub:\n"
                            "   - `git push origin week0-<your-name>`\n"
                            "2. Open a Pull Request (PR) against the main branch of the original repo.\n"
                            "3. Add a clear title, description, and apply the labels: workshop, git, high-priority\n"
                            "4. If you have permission, merge your own PR; otherwise, request a review.\n\n"
                            "**Deliverables:**\n"
                            "- Link to your opened (and merged, if possible) Pull Request."
                        ),
                        "labels": ["workshop", "git", "high-priority"],
                        "assignees": [],
                        "milestone": "Git & GitHub Workflow"
                    },
                    {
                        "title": "Peer Review: Review a Classmate’s Pull Request",
                        "body": (
                            "1. Find a classmate’s Pull Request (PR) for the Week 0 assignment in the repository.\n"
                            "2. Review their code and leave constructive feedback:\n"
                            "   - Is the code clear and correct?\n"
                            "   - Does it follow the instructions?\n"
                            "   - Are there any suggestions for improvement?\n"
                            "3. Approve the PR if it meets the requirements, or request changes if needed.\n"
                            "4. Mark this task as complete by posting a link to the PR you reviewed in the Element channel or as a comment on your own PR.\n\n"
                            "**Deliverables:**\n"
                            "- A link to the PR you reviewed and a brief summary of your feedback."
                        ),
                        "labels": ["review", "git", "collaboration", "medium-priority"],
                        "assignees": [],
                        "milestone": "Git & GitHub Workflow"
                    }
                ]
            },
        }
    
    def create_milestone(self, week: str) -> Optional[int]:
        """Create milestone for the week if it doesn't exist"""
        milestone_title = f"Week {week}"
        
        # Check if milestone already exists
        for milestone in self.repo.get_milestones(state='open'):
            if milestone.title == milestone_title:
                return milestone.number
        
        # Create new milestone
        try:
            due_date = datetime.now() + timedelta(weeks=int(week))
            milestone = self.repo.create_milestone(
                title=milestone_title,
                description=f"Tasks for Week {week} of the Generative AI Course",
                due_on=due_date
            )
            print(f"Created milestone: {milestone_title}")
            return milestone.number
        except GithubException as e:
            print(f"Error creating milestone: {e}")
            return None
    
    def create_labels(self):
        """Create labels if they don't exist"""
        labels_to_create = [
            {"name": "lecture", "color": "0366d6", "description": "Lecture materials"},
            {"name": "workshop", "color": "28a745", "description": "Workshop exercises"},
            {"name": "assignment", "color": "ffa500", "description": "Student assignments"},
            {"name": "documentation", "color": "0075ca", "description": "Documentation updates"},
            {"name": "high-priority", "color": "d73a4a", "description": "High priority tasks"},
            {"name": "medium-priority", "color": "fbca04", "description": "Medium priority tasks"},
            {"name": "low-priority", "color": "0e8a16", "description": "Low priority tasks"},
            {"name": "bug", "color": "d73a4a", "description": "Something isn't working"},
            {"name": "enhancement", "color": "a2eeef", "description": "New feature or request"},
            {"name": "good first issue", "color": "7057ff", "description": "Good for newcomers"},
            {"name": "help wanted", "color": "008672", "description": "Extra attention is needed"},
        ]
        
        existing_labels = {label.name for label in self.repo.get_labels()}
        
        for label in labels_to_create:
            if label["name"] not in existing_labels:
                try:
                    self.repo.create_label(**label)
                    print(f"Created label: {label['name']}")
                except GithubException as e:
                    print(f"Error creating label {label['name']}: {e}")
    
    def generate_tasks(self, week: str, task_type: str = "all"):
        """Generate tasks for the specified week"""
        if week not in self.week_templates:
            print(f"Error: No template found for week {week}")
            return

        # Create milestone (ignore the returned value)
        self.create_milestone(week)

        # Get the Milestone object (not just the number)
        milestone_obj = None
        for m in self.repo.get_milestones(state='open'):
            if m.title == f"Week {week}":
                milestone_obj = m
                break

        # Create labels
        self.create_labels()

        # Get tasks for the week
        week_data = self.week_templates[week]
        tasks = week_data["tasks"]

        # Filter tasks by type if specified
        if task_type != "all":
            tasks = [task for task in tasks if task_type in task["labels"]]

        created_issues = []

        for task in tasks:
            try:
                issue_kwargs = {
                    "title": task["title"],
                    "body": task["body"],
                    "labels": task["labels"],
                    "assignees": task["assignees"],
                }
                if milestone_obj is not None:
                    issue_kwargs["milestone"] = milestone_obj
                issue = self.repo.create_issue(**issue_kwargs)
                created_issues.append(issue)
                print(f"Created issue: {issue.title} (#{issue.number})")
            except Exception as e:
                print(f"Error creating issue '{task['title']}': {e}")

        print(f"\nCreated {len(created_issues)} issues for Week {week}")
        return created_issues


def main():
    parser = argparse.ArgumentParser(description="Generate GitHub issues for weekly tasks")
    parser.add_argument("--week", required=True, help="Week number (1-8)")
    parser.add_argument("--type", default="all", choices=["all", "lecture", "workshop", "assignment", "documentation"],
                       help="Type of tasks to generate")
    parser.add_argument("--token", required=True, help="GitHub token")
    parser.add_argument("--repo", default="NERD-Community-Ethiopia/generative-ai-course",
                       help="Repository name (owner/repo)")
    
    args = parser.parse_args()
    
    # Validate week number
    if not args.week.isdigit() or int(args.week) < 0 or int(args.week) > 8:
        print("Error: Week number must be between 0 and 8")
        sys.exit(1)
    
    # Create task generator
    generator = TaskGenerator(args.token, args.repo)
    
    # Generate tasks
    generator.generate_tasks(args.week, args.type)


if __name__ == "__main__":
    main() 