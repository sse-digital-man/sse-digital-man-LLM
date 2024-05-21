import websockets
import asyncio
import re
import json


def preprocess(input_string):
    # 将连续空格替换为单个空格
    cleaned_string = re.sub(r'\s+', ' ', input_string)
    # 删除URLs
    cleaned_string = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '',
                            cleaned_string)
    # 删除表情符号
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    cleaned_string = emoji_pattern.sub(r'', cleaned_string)
    # 删除表情符号的文字提示
    text_pattern = re.compile(r'\[.*?\]')
    cleaned_string = text_pattern.sub(r'', cleaned_string)
    return cleaned_string


async def revmsg():
    ws_url = 'ws://127.0.0.1:9999'
    async with websockets.connect(ws_url) as websocket:
        while True:
            recv_msg = await websocket.recv()
            recv_msg_json = json.loads(recv_msg)
            if(recv_msg_json['type'] == 'ChatMessage'):
                clean_text = preprocess(recv_msg_json['content'])
                yield f"{clean_text}"
