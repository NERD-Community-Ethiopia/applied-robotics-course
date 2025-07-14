#!/usr/bin/env python3
"""
Student Submission Checker

This script validates student submissions to ensure they meet the course requirements.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
import argparse


class SubmissionChecker:
    """Check student submissions for compliance with course requirements."""
    
    def __init__(self, submission_path: str):
        self.submission_path = Path(submission_path)
        self.errors = []
        self.warnings = []
        self.passed = True
    
    def check_directory_structure(self) -> bool:
        """Check if the submission follows the required directory structure."""
        print("🔍 Checking directory structure...")
        
        # Check if submission path exists
        if not self.submission_path.exists():
            self.errors.append(f"Submission path does not exist: {self.submission_path}")
            return False
        
        # Check for required files
        required_files = ["README.md"]
        for file in required_files:
            file_path = self.submission_path / file
            if not file_path.exists():
                self.errors.append(f"Missing required file: {file}")
                self.passed = False
        
        # Check for Python files
        python_files = list(self.submission_path.glob("*.py"))
        if not python_files:
            self.warnings.append("No Python files found in submission")
        
        return True
    
    def check_readme(self) -> bool:
        """Check if README.md meets requirements."""
        print("📖 Checking README.md...")
        
        readme_path = self.submission_path / "README.md"
        if not readme_path.exists():
            self.errors.append("README.md not found")
            return False
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for required sections
            required_sections = [
                "## Environment Setup",
                "## Completed Exercises",
                "## Challenges Faced",
                "## Learning Outcomes"
            ]
            
            for section in required_sections:
                if section not in content:
                    self.warnings.append(f"Missing section in README: {section}")
            
            # Check minimum content length
            if len(content.strip()) < 200:
                self.warnings.append("README.md seems too short (less than 200 characters)")
            
        except Exception as e:
            self.errors.append(f"Error reading README.md: {e}")
            return False
        
        return True
    
    def check_python_code(self) -> bool:
        """Check Python code quality and structure."""
        print("🐍 Checking Python code...")
        
        python_files = list(self.submission_path.glob("*.py"))
        if not python_files:
            return True  # No Python files to check
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basic syntax check
                try:
                    compile(content, py_file.name, 'exec')
                except SyntaxError as e:
                    self.errors.append(f"Syntax error in {py_file.name}: {e}")
                    self.passed = False
                
                # Check for docstrings
                if 'def ' in content and '"""' not in content and "'''" not in content:
                    self.warnings.append(f"Consider adding docstrings to functions in {py_file.name}")
                
                # Check for imports
                if 'import ' not in content and 'from ' not in content:
                    self.warnings.append(f"No imports found in {py_file.name}")
                
            except Exception as e:
                self.errors.append(f"Error reading {py_file.name}: {e}")
                self.passed = False
        
        return True
    
    def check_requirements(self) -> bool:
        """Check if requirements.txt exists and is valid."""
        print("📦 Checking requirements.txt...")
        
        req_path = self.submission_path / "requirements.txt"
        if req_path.exists():
            try:
                with open(req_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if file has content
                if not content.strip():
                    self.warnings.append("requirements.txt is empty")
                
                # Check for common required packages
                common_packages = ['langchain', 'openai', 'python-dotenv']
                for package in common_packages:
                    if package not in content:
                        self.warnings.append(f"Consider adding {package} to requirements.txt")
                
            except Exception as e:
                self.errors.append(f"Error reading requirements.txt: {e}")
                return False
        else:
            self.warnings.append("No requirements.txt found")
        
        return True
    
    def check_file_size(self) -> bool:
        """Check for reasonable file sizes."""
        print("📏 Checking file sizes...")
        
        max_size = 10 * 1024 * 1024  # 10MB
        
        for file_path in self.submission_path.rglob("*"):
            if file_path.is_file():
                try:
                    size = file_path.stat().st_size
                    if size > max_size:
                        self.warnings.append(f"Large file detected: {file_path.name} ({size / 1024 / 1024:.1f}MB)")
                except Exception as e:
                    self.warnings.append(f"Could not check size of {file_path.name}: {e}")
        
        return True
    
    def run_all_checks(self) -> Dict:
        """Run all submission checks."""
        print(f"🚀 Starting submission check for: {self.submission_path}")
        print("=" * 50)
        
        checks = [
            self.check_directory_structure,
            self.check_readme,
            self.check_python_code,
            self.check_requirements,
            self.check_file_size
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                self.errors.append(f"Error during {check.__name__}: {e}")
                self.passed = False
        
        return self.generate_report()
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive report."""
        report = {
            "passed": self.passed,
            "errors": self.errors,
            "warnings": self.warnings,
            "summary": {
                "total_errors": len(self.errors),
                "total_warnings": len(self.warnings),
                "status": "PASS" if self.passed else "FAIL"
            }
        }
        
        print("\n" + "=" * 50)
        print("📊 SUBMISSION CHECK REPORT")
        print("=" * 50)
        
        if self.passed:
            print("✅ Submission check PASSED")
        else:
            print("❌ Submission check FAILED")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        print(f"\n📈 Summary:")
        print(f"  • Total Errors: {len(self.errors)}")
        print(f"  • Total Warnings: {len(self.warnings)}")
        print(f"  • Status: {report['summary']['status']}")
        
        return report


def main():
    """Main function to run the submission checker."""
    parser = argparse.ArgumentParser(description="Check student submission compliance")
    parser.add_argument("submission_path", help="Path to the submission directory")
    parser.add_argument("--output", "-o", help="Output file for JSON report")
    
    args = parser.parse_args()
    
    # Run the checker
    checker = SubmissionChecker(args.submission_path)
    report = checker.run_all_checks()
    
    # Save report if output file specified
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            print(f"\n📄 Report saved to: {args.output}")
        except Exception as e:
            print(f"Error saving report: {e}")
    
    # Exit with appropriate code
    sys.exit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main() 