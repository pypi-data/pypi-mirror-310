"""
Core functionality for converting markdown to code files
This module is maintained for backward compatibility.
The actual implementation has been moved to the converter package.
"""
from .converter.core import MarkdownConverter

__all__ = ['MarkdownConverter']
