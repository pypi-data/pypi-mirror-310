"""
Core functionality for converting markdown to code files
"""
import os
import logging
from pathlib import Path
from ..config import Config
from ..backup import GitBackup
from .file_utils import ensure_directory
from .markdown_utils import extract_file_content

class MarkdownConverter:
    def __init__(self, input_file, output_dir='.', config=None):
        self.input_file = input_file
        self.output_dir = output_dir
        self.config = config or Config()
        # Create input file directory if it doesn't exist
        ensure_directory(self.input_file)
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

    def preview(self):
        """Preview what files will be generated without creating them."""
        try:
            # Create input file directory if it doesn't exist
            ensure_directory(self.input_file)
            
            with open(self.input_file, 'r', encoding='utf-8') as f:
                content = f.read()

            output_path = Path(self.output_dir)
            preview_info = {
                'directories': [],
                'files': [],
                'conflicts': []
            }

            # Extract file content first to get actual files
            files_content = extract_file_content(content)
            
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
            # Create input file directory if it doesn't exist
            ensure_directory(self.input_file)
            
            with open(self.input_file, 'r', encoding='utf-8') as f:
                content = f.read()

            output_path = Path(self.output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            files_content = extract_file_content(content)
            created_files = []

            for filename, file_content in files_content.items():
                file_path = output_path / filename
                ensure_directory(str(file_path))

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
