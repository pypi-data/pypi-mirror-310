"""
Markdown parsing utilities for markdown to code conversion
"""
import re
from .constants import COMMENT_PATTERNS
from .file_utils import is_valid_filename

def is_markdown_heading(line):
    """Check if a line is a markdown heading."""
    if not line:
        return False
    
    # Check if line contains a valid file path
    stripped = line.lstrip('#').strip()
    if is_valid_filename(stripped):
        return False
        
    # ATX headings (# Heading)
    if re.match(r'^#+\s+(?!filename:)', line):
        return True
        
    return False

def is_comment_pattern(text):
    """Check if text matches common comment patterns."""
    text_lower = text.lower()
    return any(pattern in text_lower for pattern in COMMENT_PATTERNS)

def extract_filename_from_line(line):
    """Extract filename from a line."""
    if not line:
        return None

    # Skip code blocks
    if line.strip().startswith('```') or line.strip().endswith('```'):
        return None

    # Try explicit filename marker first
    explicit_pattern = r'(?:^|\n)(?:#|//|/\*|<!--)\s*filename:\s*((?:[\w\-]+/)*[\w\-]+\.[a-zA-Z0-9]+)'
    explicit_match = re.search(explicit_pattern, line.strip())
    if explicit_match:
        filename = explicit_match.group(1).strip()
        if is_valid_filename(filename):
            return filename

    # Check for file path in comment
    # Must start with exactly "# " at the beginning of the line
    if re.match(r'^#\s+[\w\-./]+$', line):
        potential_path = line[2:].strip()  # Remove "# " prefix
        
        # Skip if it looks like a comment
        if is_comment_pattern(potential_path):
            return None
            
        # Must contain a file extension
        if '.' not in potential_path:
            return None
            
        # Must be a valid filename
        if not is_valid_filename(potential_path):
            return None
            
        return potential_path

    return None

def extract_file_content(markdown_content):
    """Extract file content from markdown code blocks and comments."""
    files_content = {}
    lines = markdown_content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
        
        # Try to extract filename from the line
        filename = extract_filename_from_line(line)
        
        if filename:
            content_lines = []
            i += 1  # Skip the filename line
            
            # Collect lines until we find another filename marker or markdown heading
            while i < len(lines):
                current_line = lines[i].rstrip()
                
                # Stop at next filename marker or markdown heading
                if (extract_filename_from_line(current_line) is not None or 
                    is_markdown_heading(current_line)):
                    break
                
                # Skip empty lines at the start of content
                if not content_lines and not current_line:
                    i += 1
                    continue
                    
                # Add the line to content
                content_lines.append(current_line)
                i += 1
            
            # Only add file if we have content
            if content_lines:
                # Remove trailing empty lines
                while content_lines and not content_lines[-1]:
                    content_lines.pop()
                
                content = '\n'.join(content_lines).strip()
                if content:
                    files_content[filename] = content
        else:
            i += 1
    
    return files_content
