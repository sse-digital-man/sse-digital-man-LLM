import websockets
import asyncio
import re


async def test():
    ws_url = 'ws://127.0.0.1:9999'
    async with websockets.connect(ws_url) as websocket:
        while True:
            recv_msg = await websocket.recv()
            index = recv_msg.find('content')
            recv_text = recv_msg[index+11:len(recv_msg)-2]
            clean_text = preprocess(recv_text)
            print(clean_text)


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
    return cleaned_string


asyncio.get_event_loop().run_until_complete(test())
