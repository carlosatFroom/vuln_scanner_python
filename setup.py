#!/usr/bin/env python3
"""
Setup script for Python Package Vulnerability Scanner
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies for the scanner"""
    dependencies = [
        'requests',
        'safety',
        'pip-audit'
    ]
    
    print("Installing scanner dependencies...")
    for dep in dependencies:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                          check=True)
            print(f"✓ {dep} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {dep}: {e}")
            return False
    
    return True

def main():
    """Main setup function"""
    print("Setting up Python Package Vulnerability Scanner...")
    
    if install_dependencies():
        print("\n✓ Setup completed successfully!")
        print("\nUsage:")
        print("  python vulnerability_scanner.py --requirements requirements.txt")
        print("  python vulnerability_scanner.py --requirements requirements.txt --output report.txt")
    else:
        print("\n✗ Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()