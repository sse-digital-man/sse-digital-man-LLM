import sys
sys.path.append('.')

from openai import OpenAI
from config import api_config

api_conf = api_config.Api_config()
client = OpenAI(api_key=api_conf.openai_key)

# 持续多轮对话，直到输入exit退出
user_input = ""
msgs = [{"role": "system", "content": "你好!"}]

while user_input != "exit":
    user_input = input()
    msgs.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=msgs,
        temperature=0
    )
    answer = response.choices[0].message.content
    print(answer + "\n")
    msgs.append({"role": "assistant", "content": answer})