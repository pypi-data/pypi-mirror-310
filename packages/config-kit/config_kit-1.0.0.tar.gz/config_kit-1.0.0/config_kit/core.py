import sys
from pathlib import Path
from configparser import ConfigParser
import loguru

from config_kit import util, DEFAULT_CONFIG_FILE, DEFAULT_SECTION


class ConfigKit(object):
    def __init__(self, config_file=DEFAULT_CONFIG_FILE, section=DEFAULT_SECTION, log_level='INFO'):
        self.config_file = Path(config_file).expanduser()
        self.section = section
        self._config = None
        self.config_changed = False
        self.logger = loguru.logger
        self.logger.add(sys.stdout, level=log_level)

    @property
    def config(self):
        if self._config is None:
            self._config = ConfigParser()
            if self.config_file.exists():
                self.logger.debug(f'load config file: {self.config_file}')
                self._config.read(self.config_file)
        return self._config
    
    def get(self, key):
        if self.config.has_option(self.section, key):
            return self.config.get(self.section, key)
        return None
    
    def set(self, key, value):
        if not self.config.has_section(self.section):
            self.logger.debug(f'add config section: {self.section}')
            self.config.add_section(self.section)
        
        self.config.set(self.section, key, value)
        self.config_changed = True

    def remove(self, key):
        if self.config.has_option(self.section, key):
            self.config.remove_option(self.section, key)
            self.config_changed = True

    def save(self):
        if self.config_changed:
            with util.safe_open(self.config_file, 'w') as out:
                self.config.write(out)
            self.logger.debug(f'save config file: {self.config_file}')

    def __getattr__(self, key):
        return self.get(key)

    def __delattr__(self, key):
        self.remove(key)
    
    def __setattr__(self, key, value):
        if key in ['_config', 'config_file', 'section', 'config_changed', 'logger']:
            super().__setattr__(key, value)
        else:
            self.set(key, value)

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.save()


if __name__ == '__main__':
    ck = ConfigKit('test.ini')
    # ck.name = 'admin'
    # ck.password = '123456'
    # ck.save()
    print(ck.name, ck.password)