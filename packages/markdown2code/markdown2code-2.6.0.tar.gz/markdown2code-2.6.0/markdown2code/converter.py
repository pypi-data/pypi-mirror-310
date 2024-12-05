"""
Core functionality for converting markdown to code files
"""
import os
import re
import logging
from pathlib import Path
from .config import Config
from .backup import GitBackup

class MarkdownConverter:
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

    def __init__(self, input_file, output_dir='.', config=None):
        self.input_file = input_file
        self.output_dir = output_dir
        self.config = config or Config()
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging based on configuration."""
        log_config = self.config.get_logging_config()
        logging.basicConfig(
            level=getattr(logging, log_config['level'].upper()),
            format=log_config['format']
        )
        self.logger = logging.getLogger(__name__)

    def _create_backup(self):
        """Create a backup of the current state."""
        try:
            backup = GitBackup(self.output_dir)
            branch_name = backup.create_backup(
                message="Auto-backup before markdown2code conversion"
            )
            self.logger.info(f"Created backup in branch: {branch_name}")
            return branch_name
        except Exception as e:
            self.logger.error(f"Failed to create backup: {str(e)}")
            raise

    @classmethod
    def is_valid_filename(cls, filename):
        """Check if a filename is valid based on common patterns and extensions."""
        if not filename:
            return False

        # Remove any leading/trailing whitespace and path separators
        filename = filename.strip().strip('/')
            
        # Check if it's a known filename
        if filename in cls.COMMON_FILENAMES:
            return True
            
        # Check if it has a known extension
        _, ext = os.path.splitext(filename)
        if ext in cls.COMMON_EXTENSIONS:
            return True
            
        # Check if it's a path with a known filename or extension
        if '/' in filename:
            parts = filename.split('/')
            basename = parts[-1]
            if basename in cls.COMMON_FILENAMES:
                return True
            _, ext = os.path.splitext(basename)
            if ext in cls.COMMON_EXTENSIONS:
                return True
                
        return False

    @classmethod
    def is_markdown_heading(cls, line):
        """Check if a line is a markdown heading."""
        if not line:
            return False
        
        # Check if line contains a valid file path
        stripped = line.lstrip('#').strip()
        if cls.is_valid_filename(stripped):
            return False
            
        # ATX headings (# Heading)
        if re.match(r'^#+\s+(?!filename:)', line):
            return True
            
        return False

    @classmethod
    def extract_filename_from_line(cls, line):
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
            if cls.is_valid_filename(filename):
                return filename

        # Check for file path in comment
        if line.strip().startswith('#'):
            potential_path = line.lstrip('#').strip()
            if cls.is_valid_filename(potential_path):
                return potential_path

        return None

    def extract_file_content(self, markdown_content):
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
            filename = self.extract_filename_from_line(line)
            self.logger.debug(f"Processing line: {line}")
            self.logger.debug(f"Extracted filename: {filename}")
            
            if filename:
                content_lines = []
                i += 1  # Skip the filename line
                
                # Collect lines until we find another filename marker or markdown heading
                while i < len(lines):
                    current_line = lines[i].rstrip()
                    
                    # Stop at next filename marker or markdown heading
                    if (self.extract_filename_from_line(current_line) is not None or 
                        self.is_markdown_heading(current_line)):
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
                        self.logger.debug(f"Adding file {filename} with content length: {len(content)}")
                        files_content[filename] = content
            else:
                i += 1
        
        self.logger.debug(f"Extracted {len(files_content)} files: {list(files_content.keys())}")
        return files_content

    @staticmethod
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

    @staticmethod
    def ensure_directory(file_path):
        """Create directories for the given file path."""
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def preview(self):
        """Preview what files will be generated without creating them."""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                content = f.read()

            output_path = Path(self.output_dir)
            preview_info = {
                'directories': [],
                'files': [],
                'conflicts': []
            }

            # Extract file content first to get actual files
            files_content = self.extract_file_content(content)
            
            # Get directories from file paths
            for filename in files_content.keys():
                dir_path = os.path.dirname(filename)
                if dir_path:
                    full_dir_path = output_path / dir_path
                    preview_info['directories'].append({
                        'path': str(full_dir_path),
                        'exists': full_dir_path.exists()
                    })

            # Check files
            for filename in files_content.keys():
                file_path = output_path / filename
                preview_info['files'].append({
                    'path': str(file_path),
                    'exists': file_path.exists()
                })
                if file_path.exists():
                    preview_info['conflicts'].append(str(file_path))

            return preview_info

        except Exception as e:
            self.logger.error(f"Preview failed: {str(e)}")
            raise

    def convert(self, force=False, backup=False):
        """Convert markdown file to code files."""
        backup_branch = None
        if backup:
            self.logger.info("Creating backup before proceeding...")
            backup_branch = self._create_backup()
            self.logger.info(f"Backup created successfully: {backup_branch}")

        preview_info = self.preview()
        
        if preview_info['conflicts'] and not force:
            self.logger.warning("\nWarning: The following files already exist:")
            for conflict in preview_info['conflicts']:
                self.logger.warning(f"- {conflict}")
            if backup_branch:
                self.logger.info(f"\nNote: These files have been backed up in branch: {backup_branch}")
            raise FileExistsError(
                "Some files already exist. Use --force to overwrite or choose a different output directory."
            )

        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                content = f.read()

            output_path = Path(self.output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            files_content = self.extract_file_content(content)
            created_files = []

            for filename, file_content in files_content.items():
                file_path = output_path / filename
                self.ensure_directory(str(file_path))

                self.logger.info(f"Creating file: {file_path}")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_content + '\n')

                if filename.endswith('.sh'):
                    os.chmod(file_path, 0o755)

                created_files.append(filename)

            self.logger.info("\nCreated files:")
            for f in sorted(created_files):
                self.logger.info(f"- {f}")
            
            if backup_branch:
                self.logger.info(f"\nNote: Original state backed up in branch: {backup_branch}")
            self.logger.info("\nProject structure created successfully!")

            return created_files

        except Exception as e:
            self.logger.error(f"Conversion failed: {str(e)}")
            if backup_branch:
                self.logger.info(f"\nYou can restore the original state from backup: {backup_branch}")
            raise
