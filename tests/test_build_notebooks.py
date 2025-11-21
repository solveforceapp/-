"""
Basic tests for the notebook build script.
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path


def test_build_script_exists():
    """Verify the build script exists and is executable."""
    script_path = Path(__file__).parent.parent / "scripts" / "build_notebooks.py"
    assert script_path.exists(), "build_notebooks.py script should exist"
    assert os.access(script_path, os.X_OK), "build_notebooks.py should be executable"


def test_requirements_file_exists():
    """Verify requirements.txt exists."""
    req_path = Path(__file__).parent.parent / "requirements.txt"
    assert req_path.exists(), "requirements.txt should exist"
    
    # Check that it contains expected packages
    content = req_path.read_text()
    assert "jupyter" in content
    assert "nbconvert" in content
    assert "pytest" in content
    assert "flake8" in content
