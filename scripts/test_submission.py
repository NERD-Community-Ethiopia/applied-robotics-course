#!/usr/bin/env python3
"""
Student Submission Tester

This script runs automated tests on student submissions to verify functionality.
"""

import os
import sys
import json
import subprocess
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple, Any
import argparse
import tempfile
import shutil


class SubmissionTester:
    """Run automated tests on student submissions."""
    
    def __init__(self, submission_path: str):
        self.submission_path = Path(submission_path)
        self.test_results = []
        self.passed = True
    
    def setup_test_environment(self) -> bool:
        """Set up a clean test environment."""
        print("🔧 Setting up test environment...")
        
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        print(f"Test directory: {self.test_dir}")
        
        # Copy submission files to test directory
        try:
            for item in self.submission_path.iterdir():
                if item.is_file():
                    shutil.copy2(item, self.test_dir)
                elif item.is_dir():
                    shutil.copytree(item, self.test_dir / item.name)
        except Exception as e:
            print(f"Error copying files: {e}")
            return False
        
        return True
    
    def install_dependencies(self) -> bool:
        """Install dependencies from requirements.txt."""
        print("📦 Installing dependencies...")
        
        req_file = Path(self.test_dir) / "requirements.txt"
        if req_file.exists():
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
                    capture_output=True,
                    text=True,
                    cwd=self.test_dir
                )
                
                if result.returncode != 0:
                    print(f"Warning: pip install failed: {result.stderr}")
                    return False
                
                print("Dependencies installed successfully")
                return True
            except Exception as e:
                print(f"Error installing dependencies: {e}")
                return False
        else:
            print("No requirements.txt found, skipping dependency installation")
            return True
    
    def test_python_imports(self) -> Dict[str, Any]:
        """Test if Python files can be imported without errors."""
        print("🔍 Testing Python imports...")
        
        results = {"passed": True, "errors": [], "files_tested": []}
        
        python_files = list(Path(self.test_dir).glob("*.py"))
        for py_file in python_files:
            try:
                # Try to import the module
                spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    results["files_tested"].append(str(py_file.name))
                    print(f"✅ Successfully imported: {py_file.name}")
            except Exception as e:
                results["errors"].append(f"Import error in {py_file.name}: {e}")
                results["passed"] = False
                print(f"❌ Import failed: {py_file.name} - {e}")
        
        return results
    
    def test_basic_functionality(self) -> Dict[str, Any]:
        """Test basic functionality of the submission."""
        print("🧪 Testing basic functionality...")
        
        results = {"passed": True, "errors": [], "tests_run": 0}
        
        # Look for main functions or entry points
        python_files = list(Path(self.test_dir).glob("*.py"))
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Test if file has a main function
                if 'if __name__ == "__main__":' in content:
                    results["tests_run"] += 1
                    
                    # Try to run the file with a timeout
                    try:
                        result = subprocess.run(
                            [sys.executable, str(py_file)],
                            capture_output=True,
                            text=True,
                            timeout=30,  # 30 second timeout
                            cwd=self.test_dir
                        )
                        
                        if result.returncode == 0:
                            print(f"✅ {py_file.name} ran successfully")
                        else:
                            results["errors"].append(f"Runtime error in {py_file.name}: {result.stderr}")
                            results["passed"] = False
                            print(f"❌ {py_file.name} failed to run: {result.stderr}")
                    
                    except subprocess.TimeoutExpired:
                        results["errors"].append(f"Timeout running {py_file.name}")
                        results["passed"] = False
                        print(f"⏰ {py_file.name} timed out")
                    
                    except Exception as e:
                        results["errors"].append(f"Error running {py_file.name}: {e}")
                        results["passed"] = False
                        print(f"❌ Error running {py_file.name}: {e}")
            
            except Exception as e:
                results["errors"].append(f"Error reading {py_file.name}: {e}")
                results["passed"] = False
        
        return results
    
    def test_langchain_integration(self) -> Dict[str, Any]:
        """Test LangChain integration if present."""
        print("🔗 Testing LangChain integration...")
        
        results = {"passed": True, "errors": [], "features_tested": []}
        
        try:
            # Try to import langchain
            import langchain
            results["features_tested"].append("langchain_import")
            
            # Check for common LangChain components
            python_files = list(Path(self.test_dir).glob("*.py"))
            langchain_components = [
                "LLMChain", "ConversationChain", "PromptTemplate",
                "OpenAI", "ConversationBufferMemory"
            ]
            
            for py_file in python_files:
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for component in langchain_components:
                        if component in content:
                            results["features_tested"].append(f"uses_{component.lower()}")
                            print(f"✅ Found {component} usage in {py_file.name}")
                
                except Exception as e:
                    results["errors"].append(f"Error checking {py_file.name}: {e}")
            
            if not results["features_tested"]:
                results["warnings"] = ["No LangChain components detected"]
        
        except ImportError:
            results["warnings"] = ["LangChain not available for testing"]
        
        return results
    
    def test_code_quality(self) -> Dict[str, Any]:
        """Test code quality using basic checks."""
        print("📊 Testing code quality...")
        
        results = {"passed": True, "errors": [], "metrics": {}}
        
        python_files = list(Path(self.test_dir).glob("*.py"))
        total_lines = 0
        total_functions = 0
        total_classes = 0
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                total_lines += len(lines)
                total_functions += content.count('def ')
                total_classes += content.count('class ')
                
                # Basic quality checks
                if len(lines) > 500:
                    results["warnings"] = results.get("warnings", [])
                    results["warnings"].append(f"Large file: {py_file.name} ({len(lines)} lines)")
                
                if 'TODO' in content or 'FIXME' in content:
                    results["warnings"] = results.get("warnings", [])
                    results["warnings"].append(f"TODOs/FIXMEs found in {py_file.name}")
            
            except Exception as e:
                results["errors"].append(f"Error analyzing {py_file.name}: {e}")
        
        results["metrics"] = {
            "total_files": len(python_files),
            "total_lines": total_lines,
            "total_functions": total_functions,
            "total_classes": total_classes
        }
        
        return results
    
    def cleanup(self):
        """Clean up test environment."""
        try:
            shutil.rmtree(self.test_dir)
            print(f"🧹 Cleaned up test directory: {self.test_dir}")
        except Exception as e:
            print(f"Warning: Could not clean up test directory: {e}")
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests on the submission."""
        print(f"🚀 Starting submission tests for: {self.submission_path}")
        print("=" * 50)
        
        try:
            # Setup
            if not self.setup_test_environment():
                return {"passed": False, "error": "Failed to setup test environment"}
            
            # Install dependencies
            if not self.install_dependencies():
                print("Warning: Dependency installation failed, continuing with tests")
            
            # Run tests
            test_results = {
                "imports": self.test_python_imports(),
                "functionality": self.test_basic_functionality(),
                "langchain": self.test_langchain_integration(),
                "quality": self.test_code_quality()
            }
            
            # Generate summary
            overall_passed = all(result.get("passed", True) for result in test_results.values())
            
            report = {
                "passed": overall_passed,
                "test_results": test_results,
                "summary": {
                    "total_tests": len(test_results),
                    "passed_tests": sum(1 for r in test_results.values() if r.get("passed", True)),
                    "failed_tests": sum(1 for r in test_results.values() if not r.get("passed", True))
                }
            }
            
            return report
        
        finally:
            self.cleanup()
    
    def print_report(self, report: Dict[str, Any]):
        """Print a formatted test report."""
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS REPORT")
        print("=" * 50)
        
        if report["passed"]:
            print("✅ All tests PASSED")
        else:
            print("❌ Some tests FAILED")
        
        print(f"\n📈 Summary:")
        print(f"  • Total Tests: {report['summary']['total_tests']}")
        print(f"  • Passed: {report['summary']['passed_tests']}")
        print(f"  • Failed: {report['summary']['failed_tests']}")
        
        print(f"\n🔍 Detailed Results:")
        
        for test_name, result in report["test_results"].items():
            status = "✅ PASS" if result.get("passed", True) else "❌ FAIL"
            print(f"  • {test_name.title()}: {status}")
            
            if "errors" in result and result["errors"]:
                for error in result["errors"][:3]:  # Show first 3 errors
                    print(f"    - {error}")
            
            if "warnings" in result and result["warnings"]:
                for warning in result["warnings"][:3]:  # Show first 3 warnings
                    print(f"    ⚠️  {warning}")


def main():
    """Main function to run the submission tester."""
    parser = argparse.ArgumentParser(description="Test student submission functionality")
    parser.add_argument("submission_path", help="Path to the submission directory")
    parser.add_argument("--output", "-o", help="Output file for JSON report")
    
    args = parser.parse_args()
    
    # Run the tester
    tester = SubmissionTester(args.submission_path)
    report = tester.run_all_tests()
    
    # Print report
    tester.print_report(report)
    
    # Save report if output file specified
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            print(f"\n📄 Test report saved to: {args.output}")
        except Exception as e:
            print(f"Error saving report: {e}")
    
    # Exit with appropriate code
    sys.exit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main() 