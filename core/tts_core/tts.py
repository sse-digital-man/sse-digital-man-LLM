import sys
sys.path.append(".")

from gradio_client import Client
from pasimple import play_wav

class TTS_Core:
    def __init__(self):
        self.client = Client("http://127.0.0.1:6006/")

    def tts_generate(self, text):
        path = self.client.predict(
            text,  # str in '请填写您想生成的文本' Textbox component
            "ms",  # Literal['ms', 'iflytek'] in '请选择模型' Dropdown component
            api_name="/api"
        )

        return path
    def tts_play(self, text):
        path = self.client.predict(
            text,  # str in '请填写您想生成的文本' Textbox component
            "ms",  # Literal['ms', 'iflytek'] in '请选择模型' Dropdown component
            api_name="/api"
        )

        play_wav(path)