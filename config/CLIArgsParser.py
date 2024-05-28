import argparse

class ArgsParser:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ArgsParser, cls).__new__(cls)
            cls._instance._init()
            return cls._instance
    def _init(self):
        self.parser = argparse.ArgumentParser()
    def get_args(self):
        self.parser.add_argument('--tts', type=str, help='TTS model')
        args = self.parser.parse_args()

        self.tts_model = args.tts

        # print

args_parser = ArgsParser()