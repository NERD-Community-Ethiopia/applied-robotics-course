#!/usr/bin/env python3
"""
Dependency report generator for CI/CD pipeline.
This script analyzes dependencies and generates reports for security and updates.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class DependencyReporter:
    """Generates dependency reports for the project."""
    
    def __init__(self):
        self.report_data = {
            'timestamp': datetime.now().isoformat(),
            'outdated_packages': [],
            'security_issues': [],
            'recommendations': []
        }
    
    def get_installed_packages(self) -> List[Dict[str, str]]:
        """Get list of installed packages."""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'list', '--format=json'],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                print(f"Error getting installed packages: {result.stderr}")
                return []
        except Exception as e:
            print(f"Exception getting installed packages: {e}")
            return []
    
    def get_outdated_packages(self) -> List[Dict[str, str]]:
        """Get list of outdated packages."""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'list', '--outdated', '--format=json'],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                print(f"Error getting outdated packages: {result.stderr}")
                return []
        except Exception as e:
            print(f"Exception getting outdated packages: {e}")
            return []
    
    def check_security_vulnerabilities(self) -> List[Dict[str, Any]]:
        """Check for security vulnerabilities using safety."""
        try:
            result = subprocess.run(
                ['safety', 'check', '--json'],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                print(f"Error checking security: {result.stderr}")
                return []
        except Exception as e:
            print(f"Exception checking security: {e}")
            return []
    
    def analyze_requirements_file(self) -> Dict[str, Any]:
        """Analyze requirements.txt file."""
        requirements_file = Path('requirements.txt')
        analysis = {
            'exists': False,
            'packages': [],
            'issues': []
        }
        
        if requirements_file.exists():
            analysis['exists'] = True
            try:
                with open(requirements_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line_num, line in enumerate(lines, 1):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            analysis['packages'].append({
                                'line': line_num,
                                'package': line,
                                'has_version': '==' in line or '>=' in line or '<=' in line
                            })
                            if '==' not in line and '>=' not in line and '<=' not in line:
                                analysis['issues'].append(f"Line {line_num}: No version specified for {line}")
            except Exception as e:
                analysis['issues'].append(f"Error reading requirements.txt: {e}")
        else:
            analysis['issues'].append("requirements.txt file not found")
        
        return analysis
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Check for outdated packages
        outdated = self.get_outdated_packages()
        if outdated:
            recommendations.append(f"Consider updating {len(outdated)} outdated packages")
            for package in outdated[:5]:  # Show first 5
                recommendations.append(f"  - {package.get('name', 'Unknown')}: {package.get('version', 'Unknown')} → {package.get('latest_version', 'Unknown')}")
        
        # Check for security issues
        security_issues = self.check_security_vulnerabilities()
        if security_issues:
            recommendations.append(f"Address {len(security_issues)} security vulnerabilities")
            for issue in security_issues[:3]:  # Show first 3
                pkg_name = issue.get('package', 'Unknown')
                advisory = issue.get('advisory', 'No advisory available')
                recommendations.append(f"  - {pkg_name}: {advisory}")
        
        # Check requirements.txt
        req_analysis = self.analyze_requirements_file()
        if not req_analysis['exists']:
            recommendations.append("Create a requirements.txt file to pin dependencies")
        elif req_analysis['issues']:
            recommendations.append("Fix issues in requirements.txt:")
            recommendations.extend([f"  - {issue}" for issue in req_analysis['issues'][:3]])
        
        if not recommendations:
            recommendations.append("Dependencies are up to date and secure!")
        
        return recommendations
    
    def generate_report(self) -> str:
        """Generate comprehensive dependency report."""
        # Gather data
        installed_packages = self.get_installed_packages()
        outdated_packages = self.get_outdated_packages()
        security_issues = self.check_security_vulnerabilities()
        requirements_analysis = self.analyze_requirements_file()
        recommendations = self.generate_recommendations()
        
        # Generate markdown report
        report = f"""# Dependency Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Summary

- **Total Packages**: {len(installed_packages)}
- **Outdated Packages**: {len(outdated_packages)}
- **Security Issues**: {len(security_issues)}
- **Requirements.txt Issues**: {len(requirements_analysis['issues'])}

## 🔄 Outdated Packages

"""
        
        if outdated_packages:
            report += "| Package | Current Version | Latest Version |\n"
            report += "|---------|----------------|----------------|\n"
            for package in outdated_packages[:10]:  # Show first 10
                name = package.get('name', 'Unknown')
                current = package.get('version', 'Unknown')
                latest = package.get('latest_version', 'Unknown')
                report += f"| {name} | {current} | {latest} |\n"
            
            if len(outdated_packages) > 10:
                report += f"\n*... and {len(outdated_packages) - 10} more packages*\n"
        else:
            report += "✅ All packages are up to date!\n"
        
        report += "\n## 🔒 Security Issues\n\n"
        
        if security_issues:
            report += "| Package | Issue | Severity |\n"
            report += "|---------|-------|----------|\n"
            for issue in security_issues[:10]:  # Show first 10
                pkg_name = issue.get('package', 'Unknown')
                advisory = issue.get('advisory', 'No advisory available')
                severity = issue.get('severity', 'Unknown')
                report += f"| {pkg_name} | {advisory[:50]}... | {severity} |\n"
            
            if len(security_issues) > 10:
                report += f"\n*... and {len(security_issues) - 10} more issues*\n"
        else:
            report += "✅ No security vulnerabilities found!\n"
        
        report += "\n## 📋 Requirements.txt Analysis\n\n"
        
        if requirements_analysis['exists']:
            report += f"✅ requirements.txt found with {len(requirements_analysis['packages'])} packages\n\n"
            
            if requirements_analysis['issues']:
                report += "**Issues Found:**\n"
                for issue in requirements_analysis['issues']:
                    report += f"- {issue}\n"
            else:
                report += "✅ No issues found in requirements.txt\n"
        else:
            report += "❌ requirements.txt file not found\n"
        
        report += "\n## 💡 Recommendations\n\n"
        
        for rec in recommendations:
            report += f"- {rec}\n"
        
        report += "\n## 🛠️ Next Steps\n\n"
        
        if outdated_packages or security_issues:
            report += "1. **Update outdated packages**: Run `pip install --upgrade <package-name>`\n"
            report += "2. **Address security issues**: Update vulnerable packages\n"
            report += "3. **Update requirements.txt**: Pin all dependency versions\n"
            report += "4. **Test thoroughly**: Ensure updates don't break functionality\n"
        else:
            report += "✅ Dependencies are in good shape! Continue with regular maintenance.\n"
        
        report += "\n---\n*This report was generated automatically by the CI/CD pipeline.*"
        
        return report
    
    def save_report(self, report: str, output_file: str = 'dependency-report.md'):
        """Save report to a file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Dependency report saved to {output_file}")
    
    def save_json_data(self, output_file: str = 'dependency-data.json'):
        """Save raw data as JSON."""
        # Gather fresh data
        self.report_data['outdated_packages'] = self.get_outdated_packages()
        self.report_data['security_issues'] = self.check_security_vulnerabilities()
        self.report_data['requirements_analysis'] = self.analyze_requirements_file()
        self.report_data['recommendations'] = self.generate_recommendations()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.report_data, f, indent=2)
        print(f"Dependency data saved to {output_file}")


def main():
    """Main function to generate dependency report."""
    reporter = DependencyReporter()
    
    # Generate and save report
    report = reporter.generate_report()
    reporter.save_report(report)
    reporter.save_json_data()
    
    print("Dependency report generation completed successfully!")


if __name__ == "__main__":
    main() 