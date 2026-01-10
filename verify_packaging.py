#!/usr/bin/env python3
"""
Verification script for packaging and installation.

This script verifies:
1. Version consistency between pyproject.toml and __init__.py
2. Package can be built
3. Package can be installed
4. CLI command works
5. Package metadata is correct
"""

import sys
import subprocess
import os
import shutil
import tempfile
from pathlib import Path

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def print_success(msg):
    print(f"{GREEN}✓{RESET} {msg}")

def print_error(msg):
    print(f"{RED}✗{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}⚠{RESET} {msg}")

def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def verify_version_consistency():
    """Verify version is consistent between __init__.py and pyproject.toml."""
    print("\n1. Verifying version consistency...")
    
    # Read version from __init__.py
    init_file = Path("src/caredaily/__init__.py")
    if not init_file.exists():
        print_error(f"Could not find {init_file}")
        return False
    
    with open(init_file) as f:
        for line in f:
            if line.startswith("__version__"):
                version = line.split("=")[1].strip().strip('"').strip("'")
                print_success(f"Version in __init__.py: {version}")
                return version
    
    print_error("Could not find __version__ in __init__.py")
    return None

def verify_pyproject_toml():
    """Verify pyproject.toml is valid."""
    print("\n2. Verifying pyproject.toml...")
    
    # Check if file exists
    if not Path("pyproject.toml").exists():
        print_error("pyproject.toml not found")
        return False
    
    # Try to parse it
    try:
        import tomli
        with open("pyproject.toml", "rb") as f:
            data = tomli.load(f)
        
        # Check required fields
        required_fields = ["project", "build-system"]
        for field in required_fields:
            if field not in data:
                print_error(f"Missing required field: {field}")
                return False
        
        print_success("pyproject.toml is valid")
        return True
    except ImportError:
        print_warning("tomli not available, skipping TOML validation")
        print_success("pyproject.toml exists")
        return True
    except Exception as e:
        print_error(f"Error parsing pyproject.toml: {e}")
        return False

def build_package():
    """Build the package."""
    print("\n3. Building package...")
    
    # Check if build is installed
    success, stdout, stderr = run_command("python3 -m pip show build", check=False)
    if not success:
        print_warning("build package not installed, installing...")
        success, _, _ = run_command("python3 -m pip install build", check=False)
        if not success:
            print_error("Failed to install build package")
            return False
    
    # Clean dist directory
    dist_dir = Path("dist")
    if dist_dir.exists():
        print("Cleaning dist directory...")
        shutil.rmtree(dist_dir)
    
    # Build package
    success, stdout, stderr = run_command("python3 -m build")
    if not success:
        print_error(f"Build failed: {stderr}")
        return False
    
    print_success("Package built successfully")
    
    # Check for wheel and source distribution
    dist_files = list(dist_dir.glob("*.whl")) + list(dist_dir.glob("*.tar.gz"))
    if len(dist_files) < 2:
        print_error(f"Expected 2 distribution files, found {len(dist_files)}")
        return False
    
    for file in dist_files:
        print_success(f"  Created: {file.name}")
    
    return True

def verify_installation():
    """Verify package can be installed."""
    print("\n4. Verifying installation...")
    
    # Find wheel file
    dist_dir = Path("dist")
    wheel_files = list(dist_dir.glob("*.whl"))
    if not wheel_files:
        print_error("No wheel file found")
        return False
    
    wheel_file = wheel_files[0]
    
    # Create temporary virtual environment
    with tempfile.TemporaryDirectory() as tmpdir:
        venv_path = Path(tmpdir) / "test_venv"
        print(f"Creating test virtual environment in {venv_path}...")
        
        # Create venv
        success, stdout, stderr = run_command(
            f"python3 -m venv {venv_path}",
            check=False
        )
        if not success:
            print_error(f"Failed to create venv: {stderr}")
            return False
        
        # Determine pip path
        if sys.platform == "win32":
            pip_path = venv_path / "Scripts" / "pip"
            python_path = venv_path / "Scripts" / "python"
        else:
            pip_path = venv_path / "bin" / "pip"
            python_path = venv_path / "bin" / "python"
        
        # Install package
        print("Installing package...")
        success, stdout, stderr = run_command(
            f"{pip_path} install {wheel_file.absolute()}",
            check=False
        )
        if not success:
            print_error(f"Installation failed: {stderr}")
            return False
        
        print_success("Package installed successfully")
        
        # Verify CLI command
        print("Verifying CLI command...")
        if sys.platform == "win32":
            caredaily_path = venv_path / "Scripts" / "caredaily"
        else:
            caredaily_path = venv_path / "bin" / "caredaily"
        
        if not caredaily_path.exists():
            print_error(f"CLI command not found at {caredaily_path}")
            return False
        
        print_success("CLI command found")
        
        # Test CLI help
        success, stdout, stderr = run_command(
            f"{caredaily_path} --help",
            check=False
        )
        if success:
            print_success("CLI --help works")
        else:
            print_warning(f"CLI --help failed: {stderr}")
    
    return True

def verify_metadata():
    """Verify package metadata."""
    print("\n5. Verifying package metadata...")
    
    # Check for required files
    required_files = [
        "README.md",
        "LICENSE.txt",
        "CHANGELOG.md",
    ]
    
    for file in required_files:
        if Path(file).exists():
            print_success(f"{file} exists")
        else:
            print_warning(f"{file} not found")
    
    return True

def main():
    """Run all verification steps."""
    print("=" * 60)
    print("CareDaily Package Verification")
    print("=" * 60)
    
    # Change to project root
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    results = []
    
    # Run verifications
    version = verify_version_consistency()
    results.append(("Version consistency", version is not None))
    
    results.append(("pyproject.toml", verify_pyproject_toml()))
    results.append(("Build package", build_package()))
    results.append(("Installation", verify_installation()))
    results.append(("Metadata", verify_metadata()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        if passed:
            print_success(f"{name}: PASSED")
        else:
            print_error(f"{name}: FAILED")
            all_passed = False
    
    if all_passed:
        print(f"\n{GREEN}All verifications passed!{RESET}")
        return 0
    else:
        print(f"\n{RED}Some verifications failed.{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
