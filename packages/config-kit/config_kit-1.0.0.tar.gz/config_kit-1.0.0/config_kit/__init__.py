import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
version_info = json.load(BASE_DIR.joinpath('version.json').open())


DEFAULT_CONFIG_FILE = Path('~/.config_kit.ini').expanduser()
DEFAULT_SECTION = 'common'

__version__ = version_info['version']
