import sys
sys.path.append('.')

from configparser import ConfigParser

class api_config_info:
    def __init__(self):
        system_config = ConfigParser()
        system_config.read('system.conf')

        self.openai_key = system_config.get('keys', 'openai_key')