#!/usr/bin/env python3
"""
Release management script for PyP6XER.
Helps with version bumping, changelog generation, and release preparation.
"""

import os
import sys
import re
import subprocess
from datetime import datetime
from pathlib import Path

def get_current_version():
    """Get current version from xerparser/__init__.py"""
    init_file = Path("xerparser/__init__.py")
    content = init_file.read_text()
    match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    raise ValueError("Version not found in xerparser/__init__.py")

def update_version(new_version):
    """Update version in all relevant files"""
    files_to_update = [
        ("xerparser/__init__.py", r'__version__ = ["\']([^"\']+)["\']', f'__version__ = "{new_version}"'),
        ("setup.py", r"version='([^']+)'", f"version='{new_version}'"),
        ("docs/source/conf.py", r"version = '([^']+)'", f"version = '{new_version}'"),
        ("docs/source/conf.py", r"release = '([^']+)'", f"release = '{new_version}'"),
    ]
    
    for file_path, pattern, replacement in files_to_update:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            
            new_content = re.sub(pattern, replacement, content)
            
            with open(file_path, 'w') as f:
                f.write(new_content)
            
            print(f"✅ Updated version in {file_path}")

def run_tests():
    """Run tests to ensure everything works"""
    print("🧪 Running tests...")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ All tests passed!")
        return True
    else:
        print("❌ Tests failed:")
        print(result.stdout)
        print(result.stderr)
        return False

def build_package():
    """Build the package"""
    print("📦 Building package...")
    
    # Clean previous builds
    subprocess.run([sys.executable, "-c", "import shutil; shutil.rmtree('dist', ignore_errors=True)"])
    subprocess.run([sys.executable, "-c", "import shutil; shutil.rmtree('build', ignore_errors=True)"])
    
    # Build
    result = subprocess.run([sys.executable, "-m", "build"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Package built successfully!")
        return True
    else:
        print("❌ Package build failed:")
        print(result.stdout)
        print(result.stderr)
        return False

def check_package():
    """Check the built package"""
    print("🔍 Checking package...")
    result = subprocess.run([sys.executable, "-m", "twine", "check", "dist/*"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Package check passed!")
        return True
    else:
        print("❌ Package check failed:")
        print(result.stdout)
        print(result.stderr)
        return False

def create_git_tag(version):
    """Create git tag for the release"""
    tag_name = f"v{version}"
    
    # Check if tag already exists
    result = subprocess.run(["git", "tag", "-l", tag_name], capture_output=True, text=True)
    if tag_name in result.stdout:
        print(f"⚠️  Tag {tag_name} already exists")
        return False
    
    # Create tag
    result = subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Release version {version}"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Created git tag {tag_name}")
        return True
    else:
        print(f"❌ Failed to create git tag:")
        print(result.stderr)
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="PyP6XER Release Management")
    parser.add_argument("action", choices=["bump", "build", "check", "tag", "release"], 
                       help="Action to perform")
    parser.add_argument("--version", help="New version number (for bump)")
    parser.add_argument("--type", choices=["patch", "minor", "major"], 
                       help="Version bump type")
    
    args = parser.parse_args()
    
    if args.action == "bump":
        current = get_current_version()
        print(f"Current version: {current}")
        
        if args.version:
            new_version = args.version
        elif args.type:
            # Simple version bumping logic
            parts = current.split('.')
            if args.type == "patch":
                parts[2] = str(int(parts[2]) + 1)
            elif args.type == "minor":
                parts[1] = str(int(parts[1]) + 1)
                parts[2] = "0"
            elif args.type == "major":
                parts[0] = str(int(parts[0]) + 1)
                parts[1] = "0"
                parts[2] = "0"
            new_version = ".".join(parts)
        else:
            print("Please specify --version or --type")
            return 1
        
        print(f"Updating to version: {new_version}")
        update_version(new_version)
        
    elif args.action == "build":
        if not build_package():
            return 1
            
    elif args.action == "check":
        if not check_package():
            return 1
            
    elif args.action == "tag":
        version = get_current_version()
        if not create_git_tag(version):
            return 1
            
    elif args.action == "release":
        print("🚀 Preparing release...")
        
        # Run full release process
        current = get_current_version()
        print(f"Releasing version: {current}")
        
        # Run tests
        if not run_tests():
            print("❌ Release aborted due to test failures")
            return 1
        
        # Build package
        if not build_package():
            print("❌ Release aborted due to build failures")
            return 1
            
        # Check package
        if not check_package():
            print("❌ Release aborted due to package check failures")
            return 1
        
        # Create git tag
        if not create_git_tag(current):
            print("❌ Release aborted due to git tag creation failure")
            return 1
        
        print("✅ Release preparation complete!")
        print("📋 Next steps:")
        print("1. Review the changes: git log --oneline")
        print("2. Push changes: git push origin master")
        print(f"3. Push tag: git push origin v{current}")
        print("4. Create GitHub release to trigger PyPI publishing")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
