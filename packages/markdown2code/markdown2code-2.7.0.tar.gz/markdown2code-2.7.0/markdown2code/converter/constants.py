"""
Common constants and patterns used in markdown to code conversion
"""

# Common file extensions that should be recognized
COMMON_EXTENSIONS = {
    # Configuration files
    '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
    # Web files
    '.html', '.css', '.js', '.jsx', '.ts', '.tsx', '.vue',
    # Python files
    '.py', '.pyi', '.pyx',
    # Shell scripts
    '.sh', '.bash',
    # Documentation
    '.md', '.rst', '.txt',
    # Environment files
    '.env', '.env.example',
    # Requirements files
    'requirements.txt', 'requirements-dev.txt', 'requirements-test.txt',
    # Package files
    'setup.py', 'setup.cfg', 'pyproject.toml',
    # Git files
    '.gitignore', '.gitattributes',
    # Docker files
    'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml'
}

# Common filenames that should be recognized even without extensions
COMMON_FILENAMES = {
    'Dockerfile', 'Makefile', 'README', 'LICENSE', 'CHANGELOG',
    'requirements.txt', '.env', '.env.example', '.gitignore'
}

# Common comment patterns to exclude
COMMENT_PATTERNS = {
    'note:', 'todo:', 'fixme:', 'hack:', 'xxx:', 'bug:',
    'tokeny', 'próba', 'test:', 'debug:', 'warning:',
    'important:', 'attention:', 'notice:'
}
