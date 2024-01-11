import sys
sys.path.append('.')

from configparser import ConfigParser

class Api_config:
    def __init__(self):
        system_config = ConfigParser()
        system_config.read('system.conf')

        self.openai_key = system_config.get('keys', 'openai_key')

        self.ali_nls_key_id = system_config.get('keys', 'ali_nls_key_id')
        self.ali_nls_key_secret = system_config.get('keys', 'ali_nls_key_secret')
        self.ali_nls_app_key = system_config.get('keys', 'ali_nls_app_key')

        self.oss_endpoint = system_config.get('keys', 'oss_endpoint')
        self.oss_bucket_name = system_config.get('keys', 'oss_bucket_name')
