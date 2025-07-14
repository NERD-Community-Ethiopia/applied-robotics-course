#!/usr/bin/env python3
"""
Automated feedback generator for student submissions.
This script analyzes student submissions and generates constructive feedback.
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Any
import subprocess
import re


class FeedbackGenerator:
    """Generates automated feedback for student submissions."""
    
    def __init__(self):
        self.feedback = []
        self.score = 0
        self.max_score = 100
        
    def analyze_submission_structure(self, submission_path: str) -> Dict[str, Any]:
        """Analyze the structure of a student submission."""
        path = Path(submission_path)
        analysis = {
            'has_readme': False,
            'has_requirements': False,
            'has_code_files': False,
            'structure_score': 0,
            'feedback': []
        }
        
        # Check for README
        if (path / 'README.md').exists():
            analysis['has_readme'] = True
            analysis['structure_score'] += 20
            analysis['feedback'].append("✅ README.md found")
        else:
            analysis['feedback'].append("❌ Missing README.md")
        
        # Check for requirements.txt
        if (path / 'requirements.txt').exists():
            analysis['has_requirements'] = True
            analysis['structure_score'] += 15
            analysis['feedback'].append("✅ requirements.txt found")
        else:
            analysis['feedback'].append("❌ Missing requirements.txt")
        
        # Check for Python files
        python_files = list(path.glob('*.py'))
        if python_files:
            analysis['has_code_files'] = True
            analysis['structure_score'] += 25
            analysis['feedback'].append(f"✅ Found {len(python_files)} Python file(s)")
        else:
            analysis['feedback'].append("❌ No Python files found")
        
        # Check for proper directory structure
        if path.name.startswith('week-'):
            analysis['structure_score'] += 10
            analysis['feedback'].append("✅ Proper week directory naming")
        else:
            analysis['feedback'].append("⚠️ Consider using 'week-X' format for directory naming")
        
        return analysis
    
    def analyze_code_quality(self, submission_path: str) -> Dict[str, Any]:
        """Analyze code quality using various tools."""
        path = Path(submission_path)
        analysis = {
            'quality_score': 0,
            'feedback': [],
            'issues': []
        }
        
        python_files = list(path.glob('*.py'))
        if not python_files:
            return analysis
        
        # Run flake8 for code style
        try:
            result = subprocess.run(
                ['flake8', str(path), '--count', '--select=E,W', '--max-line-length=88'],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                analysis['quality_score'] += 20
                analysis['feedback'].append("✅ Code follows PEP 8 style guidelines")
            else:
                issues = result.stdout.strip().split('\n') if result.stdout else []
                analysis['issues'].extend(issues[:5])  # Show first 5 issues
                analysis['feedback'].append(f"⚠️ Found {len(issues)} style issues (showing first 5)")
        except Exception as e:
            analysis['feedback'].append(f"⚠️ Could not run style check: {e}")
        
        # Check for docstrings
        docstring_count = 0
        function_count = 0
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Simple regex to count functions and docstrings
                    functions = re.findall(r'def\s+\w+', content)
                    docstrings = re.findall(r'""".*?"""', content, re.DOTALL)
                    function_count += len(functions)
                    docstring_count += len(docstrings)
            except Exception:
                continue
        
        if function_count > 0:
            docstring_ratio = docstring_count / function_count
            if docstring_ratio >= 0.5:
                analysis['quality_score'] += 15
                analysis['feedback'].append("✅ Good documentation with docstrings")
            else:
                analysis['feedback'].append("⚠️ Consider adding more docstrings to functions")
        
        # Check for error handling
        try:
            result = subprocess.run(
                ['grep', '-r', 'try:', str(path)],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                analysis['quality_score'] += 10
                analysis['feedback'].append("✅ Error handling found in code")
            else:
                analysis['feedback'].append("⚠️ Consider adding error handling")
        except Exception:
            analysis['feedback'].append("⚠️ Could not check for error handling")
        
        return analysis
    
    def analyze_functionality(self, submission_path: str) -> Dict[str, Any]:
        """Analyze if the code is functional."""
        path = Path(submission_path)
        analysis = {
            'functionality_score': 0,
            'feedback': [],
            'tests_passed': 0,
            'tests_total': 0
        }
        
        # Check if code runs without syntax errors
        python_files = list(path.glob('*.py'))
        for py_file in python_files:
            try:
                result = subprocess.run(
                    [sys.executable, '-m', 'py_compile', str(py_file)],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    analysis['functionality_score'] += 10
                    analysis['feedback'].append(f"✅ {py_file.name} has valid Python syntax")
                else:
                    analysis['feedback'].append(f"❌ {py_file.name} has syntax errors")
            except Exception as e:
                analysis['feedback'].append(f"⚠️ Could not check {py_file.name}: {e}")
        
        # Check for test files
        test_files = list(path.glob('*test*.py')) + list(path.glob('test_*.py'))
        if test_files:
            analysis['feedback'].append(f"✅ Found {len(test_files)} test file(s)")
            analysis['functionality_score'] += 10
        else:
            analysis['feedback'].append("⚠️ No test files found - consider adding tests")
        
        return analysis
    
    def generate_overall_feedback(self, submission_path: str) -> str:
        """Generate comprehensive feedback for a submission."""
        structure_analysis = self.analyze_submission_structure(submission_path)
        quality_analysis = self.analyze_code_quality(submission_path)
        functionality_analysis = self.analyze_functionality(submission_path)
        
        total_score = (
            structure_analysis['structure_score'] +
            quality_analysis['quality_score'] +
            functionality_analysis['functionality_score']
        )
        
        feedback_md = f"""# Automated Feedback Report

## 📊 Overall Score: {total_score}/100

### 📁 Structure Analysis ({structure_analysis['structure_score']}/70)
{chr(10).join(structure_analysis['feedback'])}

### 🎯 Code Quality ({quality_analysis['quality_score']}/45)
{chr(10).join(quality_analysis['feedback'])}

### ⚙️ Functionality ({functionality_analysis['functionality_score']}/20)
{chr(10).join(functionality_analysis['feedback'])}

## 🏆 Grade Breakdown
- **Structure**: {structure_analysis['structure_score']}/70 points
- **Code Quality**: {quality_analysis['quality_score']}/45 points  
- **Functionality**: {functionality_analysis['functionality_score']}/20 points
- **Total**: {total_score}/135 points (scaled to 100)

## 📝 Recommendations

### What you did well:
"""
        
        # Add positive feedback
        positive_points = []
        if structure_analysis['has_readme']:
            positive_points.append("- Good documentation with README.md")
        if structure_analysis['has_requirements']:
            positive_points.append("- Proper dependency management")
        if quality_analysis['quality_score'] > 20:
            positive_points.append("- Code follows good style practices")
        if functionality_analysis['functionality_score'] > 10:
            positive_points.append("- Code is syntactically correct")
        
        if positive_points:
            feedback_md += "\n".join(positive_points)
        else:
            feedback_md += "- Keep working on the basics!"
        
        feedback_md += "\n\n### Areas for improvement:\n"
        
        # Add improvement suggestions
        improvements = []
        if not structure_analysis['has_readme']:
            improvements.append("- Add a comprehensive README.md file")
        if not structure_analysis['has_requirements']:
            improvements.append("- Include a requirements.txt file")
        if quality_analysis['quality_score'] < 20:
            improvements.append("- Improve code style and formatting")
        if not functionality_analysis['functionality_score']:
            improvements.append("- Fix syntax errors in your code")
        
        if improvements:
            feedback_md += "\n".join(improvements)
        else:
            feedback_md += "- Great job! Keep up the excellent work!"
        
        feedback_md += f"""

## 🔍 Detailed Issues
"""
        
        if quality_analysis['issues']:
            feedback_md += "\n".join([f"- {issue}" for issue in quality_analysis['issues']])
        else:
            feedback_md += "- No major issues found!"
        
        feedback_md += """

---
*This feedback was generated automatically. Please review and address the suggestions above.*
"""
        
        return feedback_md
    
    def save_feedback(self, feedback: str, output_file: str = 'feedback.md'):
        """Save feedback to a file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(feedback)
        print(f"Feedback saved to {output_file}")


def main():
    """Main function to generate feedback."""
    if len(sys.argv) < 2:
        print("Usage: python generate_feedback.py <submission_path>")
        sys.exit(1)
    
    submission_path = sys.argv[1]
    if not os.path.exists(submission_path):
        print(f"Error: Path {submission_path} does not exist")
        sys.exit(1)
    
    generator = FeedbackGenerator()
    feedback = generator.generate_overall_feedback(submission_path)
    generator.save_feedback(feedback)
    
    print("Feedback generation completed successfully!")


if __name__ == "__main__":
    main() 