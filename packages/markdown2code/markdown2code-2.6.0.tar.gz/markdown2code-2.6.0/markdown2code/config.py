"""
Configuration handling for markdown2code
"""
import os
import yaml
from pathlib import Path

DEFAULT_CONFIG = {
    'file_patterns': {
        'javascript': ['script.js', 'index.js', 'main.js'],
        'js': ['script.js', 'index.js', 'main.js'],
        'python': ['script.py', 'main.py', 'app.py'],
        'py': ['script.py', 'main.py', 'app.py'],
        'css': ['styles.css', 'main.css', 'app.css'],
        'html': ['index.html', 'main.html', 'app.html'],
        'java': ['Main.java', 'App.java', 'Application.java'],
        'cpp': ['main.cpp', 'app.cpp', 'program.cpp'],
        'c': ['main.c', 'app.c', 'program.c'],
        'sql': ['query.sql', 'schema.sql', 'data.sql'],
        'php': ['index.php', 'app.php', 'main.php'],
        'ruby': ['script.rb', 'app.rb', 'main.rb'],
        'go': ['main.go', 'app.go', 'program.go'],
        'rust': ['main.rs', 'lib.rs', 'program.rs'],
        'typescript': ['script.ts', 'index.ts', 'main.ts'],
        'ts': ['script.ts', 'index.ts', 'main.ts'],
        'yaml': ['config.yml', 'settings.yml', 'app.yml'],
        'yml': ['config.yml', 'settings.yml', 'app.yml'],
        'json': ['config.json', 'settings.json', 'app.json'],
        'xml': ['config.xml', 'settings.xml', 'app.xml'],
        'markdown': ['README.md', 'GUIDE.md', 'DOCS.md'],
        'md': ['README.md', 'GUIDE.md', 'DOCS.md'],
        'bash': ['script.sh', 'setup.sh', 'run.sh'],
        'sh': ['script.sh', 'setup.sh', 'run.sh'],
        'dockerfile': ['Dockerfile', 'Dockerfile.dev', 'Dockerfile.prod']
    },
    'logging': {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    },
    'output': {
        'colored': False,
        'verbose': False
    }
}

class Config:
    def __init__(self, config_dir=None):
        """Initialize configuration.
        
        Args:
            config_dir: Optional directory to look for config files (used in testing)
        """
        self.config = DEFAULT_CONFIG.copy()
        self.config_dir = config_dir
        self.load_user_config()

    def load_user_config(self):
        """Load user configuration from various locations."""
        if self.config_dir:
            config_locations = [
                Path(self.config_dir) / '.markdown2code.yml',
                Path(self.config_dir) / '.config' / 'markdown2code' / 'config.yml'
            ]
        else:
            config_locations = [
                Path.home() / '.config' / 'markdown2code' / 'config.yml',
                Path.home() / '.markdown2code.yml',
                Path.cwd() / '.markdown2code.yml'
            ]

        for config_path in config_locations:
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        user_config = yaml.safe_load(f)
                        if user_config:
                            self._merge_config(user_config)
                            break  # Stop after first successful load
                except Exception as e:
                    print(f"Warning: Failed to load config from {config_path}: {e}")

    def _merge_config(self, user_config):
        """Merge user configuration with defaults."""
        if 'file_patterns' in user_config:
            # Create a new copy of file patterns and update it
            file_patterns = self.config['file_patterns'].copy()
            file_patterns.update(user_config['file_patterns'])
            self.config['file_patterns'] = file_patterns
            
        if 'logging' in user_config:
            # Create a new copy of logging config and update it
            logging_config = self.config['logging'].copy()
            logging_config.update(user_config['logging'])
            self.config['logging'] = logging_config
            
        if 'output' in user_config:
            # Create a new copy of output config and update it
            output_config = self.config['output'].copy()
            output_config.update(user_config['output'])
            self.config['output'] = output_config

    def get_file_patterns(self, language):
        """Get file patterns for a language."""
        return self.config['file_patterns'].get(language, [f"file.{language}"])

    def get_logging_config(self):
        """Get logging configuration."""
        return self.config['logging']

    def get_output_config(self):
        """Get output configuration."""
        return self.config['output']

    @staticmethod
    def create_default_config(path=None):
        """Create a default configuration file."""
        if path is None:
            path = Path.home() / '.markdown2code.yml'
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w') as f:
            yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False)
        
        return path
