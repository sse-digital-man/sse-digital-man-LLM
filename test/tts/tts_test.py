import sys
sys.path.append(".")

from gradio_client import Client
from pasimple import play_wav

if __name__ == '__main__':
    client = Client("http://127.0.0.1:6006/")
    result = client.predict(
        "你好呀，我叫李白",  # str in '请填写您想生成的文本' Textbox component
        "ms",  # Literal['ms', 'iflytek'] in '请选择模型' Dropdown component
        api_name="/api"
    )
    print(result)

    play_wav(result)
