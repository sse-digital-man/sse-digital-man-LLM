import sys
sys.path.append(".")

from gradio_client import Client
from config.ConfigLoader import config
from config.CLIArgsParser import args_parser

class TTS_Core:
    def __init__(self):
        self.client = Client("http://127.0.0.1:6006/")
        if args_parser.tts_model == None:
            self.model = config.tts_model
        else:
            self.model = args_parser.tts_model

        print(f"TTS Model: {self.model}")


    def tts_generate(self, text):
        if self.model == "ms":
            path = self.client.predict(
                text,  # str in '请填写您想生成的文本' Textbox component
                "ms",  # Literal['ms', 'iflytek'] in '请选择模型' Dropdown component
                api_name="/api"
            )
            return path
        elif self.model == "tiejun":
            result = self.client.predict(
                    text,	# str in '输入文本内容' Textbox component
                    "tiejun",	# Literal['tiejun'] in '选择说话人' Dropdown component
                    0,	# float (numeric value between 0 and 1)
                                            # in 'SDP/DP混合比' Slider component
                    0.1,	# float (numeric value between 0.1 and 2)
                                            # in '感情' Slider component
                    0.1,	# float (numeric value between 0.1 and 2)
                                            # in '音素长度' Slider component
                    1,	# float (numeric value between 0.1 and 2)
                                            # in '语速' Slider component
                    "ZH",	# Literal['ZH'] in '选择语言' Dropdown component
                    api_name="/tts_fn"
            )
            path = result[1]
            return path
        else:
            throw('tts model not supported')

tts_core = TTS_Core()

