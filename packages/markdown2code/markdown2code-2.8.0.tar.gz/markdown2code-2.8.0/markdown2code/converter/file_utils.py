"""
File handling utilities for markdown to code conversion
"""
import os
import re
from pathlib import Path
from .constants import COMMON_EXTENSIONS, COMMON_FILENAMES

def is_valid_filename(filename):
    """Check if a filename is valid based on common patterns and extensions."""
    if not filename:
        return False

    # Remove any leading/trailing whitespace and path separators
    filename = filename.strip().strip('/')
        
    # Check if it's a known filename
    if filename in COMMON_FILENAMES:
        return True
        
    # Check if it has a known extension
    _, ext = os.path.splitext(filename)
    if ext in COMMON_EXTENSIONS:
        return True
        
    # Check if it's a path with a known filename or extension
    if '/' in filename:
        parts = filename.split('/')
        basename = parts[-1]
        if basename in COMMON_FILENAMES:
            return True
        _, ext = os.path.splitext(basename)
        if ext in COMMON_EXTENSIONS:
            return True
                
    return False

def create_directory_structure(structure_text):
    """Create a list of paths from text directory structure."""
    paths = []
    current_path = []
    
    for line in structure_text.split('\n'):
        line = line.strip()
        if not line or '```' in line:
            continue

        # Count the depth by the number of │ or ├ or └ characters
        depth = len(re.findall(r'[│├└]', line))
        
        # Remove tree characters and spaces
        path = re.sub(r'^[│├└─\s]+', '', line)
        
        if path and not path.startswith('#'):
            # Adjust current path based on depth
            current_path = current_path[:depth]
            current_path.append(path)
            
            # Create full path
            full_path = '/'.join(p.rstrip('/') for p in current_path)
            if not ('.' in path):  # It's a directory
                full_path += '/'
            paths.append(full_path)

    return paths

def ensure_directory(file_path):
    """Create directories for the given file path."""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
