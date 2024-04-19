import sys
sys.path.append(".")

from gradio_client import Client
from pasimple import play_wav

from config import api_config

class TTS_Core:
    def __init__(self):
        self.api_conf = api_config.Api_config()
        self.client = Client("http://127.0.0.1:6006/")

    def tts_generate(self, text):
        model = self.api_conf.tts_model

        if model == "ms":
            path = self.client.predict(
                text,  # str in '请填写您想生成的文本' Textbox component
                "ms",  # Literal['ms', 'iflytek'] in '请选择模型' Dropdown component
                api_name="/api"
            )
            return path
        elif model == "tiejun":
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
