import sys
sys.path.append('.')

import yaml

class ConfigLoader:
    def __init__(self):
        with open('config.yml', 'r', encoding='utf-8') as f:
            try:
                config = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(f'Error loading YAML file: {exc}')

        self.openai_key = config['api_keys']['llm']['openai_key']
        self.tts_model = config['api_config']['tts']['tts_model']
        self.answer_interval = config['ue_config']['answer_interval']
        self.db_client_port = config['chroma_db_config']['db_client_port']
        self.db_collection_name = config['chroma_db_config']['db_collection_name']
        self.db_dimension = config['chroma_db_config']['db_dimension']
        self.db_k = config['chroma_db_config']['db_k']

config = ConfigLoader()
