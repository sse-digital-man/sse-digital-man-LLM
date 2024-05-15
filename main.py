import random
import sys

sys.path.append(".")

from config import db_config
import time
from core.db_operate.DB_Operator import DbOperator
from core.db_operate.connection_handler import get_db_client
from core.llm_core.Bot import Bot as Bot
from core.tts_core.tts import TTS_Core
from utils.reload_database import reload_database

import asyncio
from front import revmsg

import pygame

print('正在启动数字人内核')
db_operator = DbOperator()
tts_core = TTS_Core()
msg_history = []

pygame.init()

async def crawler(message_queue):
    async for user_input in revmsg():
        if message_queue.qsize() > 10:
            print("Queue size is greater than 10. Waiting for 10 seconds.")
            await asyncio.sleep(10)
            continue
        print(f"[info] 用户输入: {user_input}")
        await message_queue.put(user_input)
        await asyncio.sleep(random.uniform(0.1, 0.5))


async def llm(message_queue, audio_queue):
    while True:
        user_input = await message_queue.get()
        try:
            # LLM
            search_result = db_operator.search(db_config.COLLECTION_NAME, user_input)
            bot = Bot()
            cur_prompt = bot.get_prompt(user_input, search_result)
            answer = bot.answer(cur_prompt, msg_history)
            print(answer)

            # TTS
            tts_start_time = time.time()
            print('[info] 开始生成音频')
            path = tts_core.tts_generate(answer)
            tts_end_time = time.time()
            tts_elapsed_time = tts_end_time - tts_start_time
            print(f"[info] 音频生成完成。用时{format(tts_elapsed_time, '.2f')}s")

            # 存在队列里面
            await audio_queue.put(path)
        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            message_queue.task_done()

async def play_audio(audio_queue):
    while True:
        path = await audio_queue.get()
        try:
            print('[info] 开始播放音频')
            sound = pygame.mixer.Sound(path)
            channel = pygame.mixer.Channel(0)
            channel.play(sound)
            while channel.get_busy():
                pygame.time.Clock().tick(30)
            print('[info] 结束播放')
        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            audio_queue.task_done()


async def main():
    message_queue = asyncio.Queue()
    audio_queue = asyncio.Queue()

    crawler_task = asyncio.create_task(crawler(message_queue))
    llm_task = asyncio.create_task(llm(message_queue, audio_queue))
    play_audio_task = asyncio.create_task(play_audio(audio_queue))

    await asyncio.gather(crawler_task, llm_task, play_audio_task)
    # await message_queue.join()
    # await audio_queue.join()

if __name__ == '__main__':
    # initialize

    client = get_db_client()
    collections = client.list_collections()

    if db_config.COLLECTION_NAME not in [c.name for c in collections]:
        reload_database(db_config.COLLECTION_NAME)


    print('数字人内核已启动')
    asyncio.run(main())
    # producer_task  = asyncio.get_event_loop().run_until_complete(producer(queue))

