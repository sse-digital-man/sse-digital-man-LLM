import sys

sys.path.append(".")

import asyncio
import time
import random
import pygame

from config.ConfigLoader import config
from core import websocket_server
from core.db_operate.DB_Operator import db_operator
from core.db_operate.connection_handler import get_db_client
from core.llm_core.Bot import Bot as Bot
from core.tts_core.tts import TTS_Core
from core.ue_core.ovr_lipsync.test_olipsync import LipSyncGenerator
from utils.reload_database import reload_database
from front import revmsg


print('正在启动数字人内核')
tts_core = TTS_Core()
msg_history = [] #暂未启用

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
            search_result = db_operator.search(config.db_collection_name, user_input)
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
            await audio_queue.put((path, user_input, answer))
        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            message_queue.task_done()

async def play_audio(audio_queue):
    while True:
        path, question, answer = await audio_queue.get()
        try:
            # 获取音频长度
            sound = pygame.mixer.Sound(path)
            audio_length = sound.get_length()

            # 发送问题文本给UE
            content = {'Topic': 'Unreal',
                       'Data': {'Key': 'question', 'Value': question}}

            websocket_server.get_instance().add_cmd(content)

            # 发送回答文本给UE
            content = {'Topic': 'Unreal',
                       'Data': {'Key': 'text', 'Value': answer}}

            websocket_server.get_instance().add_cmd(content)

            # 发送音频给UE
            content = {'Topic': 'Unreal',
                       'Data': {'Key': 'audio', 'Value': path, 'Text': answer,
                                'Time': audio_length, 'Type': 'interact', 'Lips':[]}}

            # 计算唇形
            print('[info] 开始计算唇形')
            lips_start_time = time.time()
            lip_sync_generator = LipSyncGenerator()
            viseme_list = lip_sync_generator.generate_visemes(path)
            consolidated_visemes = lip_sync_generator.consolidate_visemes(viseme_list)
            content["Data"]["Lips"] = consolidated_visemes
            lips_end_time = time.time()
            lips_elapsed_time = lips_end_time - lips_start_time
            print(f"[info] 唇形计算完成。用时{format(lips_elapsed_time, '.2f')}s")

            websocket_server.get_instance().add_cmd(content)

            # 等待音频播放结束
            await asyncio.sleep(audio_length)

            print('[info] 音频播放完毕')

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
    # initialize pygame
    pygame.init()

    # initialize database

    client = get_db_client()
    collections = client.list_collections()

    if config.db_collection_name not in [c.name for c in collections]:
        reload_database(config.db_collection_name)

    print('数字人内核已启动')

    # ue core
    ws_server = websocket_server.new_instance(port=10002)
    ws_server.start_server()
    web_ws_server = websocket_server.new_web_instance(port=10003)
    web_ws_server.start_server()

    web_server_instance = websocket_server.get_web_instance()
    web_server_instance.add_cmd({"liveState": 1})
    web_server_instance.add_cmd({"is_connect": True})


    print('ue内核已启动')

    asyncio.run(main())
    # producer_task  = asyncio.get_event_loop().run_until_complete(producer(queue))

