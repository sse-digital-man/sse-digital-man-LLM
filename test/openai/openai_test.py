import sys
sys.path.append('.')

from openai import OpenAI
from config import api_config

api_conf = api_config.Api_config()
client = OpenAI(api_key=api_conf.openai_key)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "你好!"},
        {"role": "user", "content": "给我讲个笑话吧"},
    ],
    temperature=0
)

print(response.choices[0].message.content)