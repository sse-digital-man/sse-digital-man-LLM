import random
import sys

sys.path.append(".")

from pymilvus import Collection, utility
from config import db_config
import time
from core.db_operate.DB_Operator import DbOperator
from core.db_operate.connection_handler import open_connection
from core.db_operate.connection_handler import close_connection
from core.llm_core.Bot import Bot as Bot
from core.tts_core.tts import TTS_Core

import asyncio
from front import revmsg

print('正在启动数字人内核')
db_operator = DbOperator()
tts_core = TTS_Core()
msg_history = []

async def producer(queue):
    count = 0
    async for user_input in revmsg():
        if queue.qsize() > 10:
            print("Queue size is greater than 10. Waiting for 10 seconds.")
            await asyncio.sleep(10)
            continue
        print(f"Producing: {user_input}")
        await queue.put(user_input)
        await asyncio.sleep(random.uniform(0.1, 0.5))


async def consumer(queue):
    while True:
        user_input = await queue.get()
        print(f"Consuming: {user_input}")

        # LLM
        search_result = db_operator.search(user_input)
        bot = Bot()
        cur_prompt = bot.get_prompt(user_input, search_result)
        answer = bot.answer(cur_prompt, msg_history)
        print(answer)

        # TTS
        path = tts_core.tts_generate(answer)

        # 存在队列里面

        queue.task_done()


async def main():
    queue = asyncio.Queue()
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))

    await asyncio.gather(producer_task, consumer_task)
    await queue.join()


if __name__ == '__main__':
    open_connection()

    # initialize

    if not utility.has_collection(db_config.COLLECTION_NAME):  # 如果collection不存在,创建collection
        create_collection(db_config.COLLECTION_NAME)

    collection = Collection(db_config.COLLECTION_NAME)

    if collection.num_entities == 0:  # 如果无embedding,创建embedding
        create_embeddings(db_config.COLLECTION_NAME)

    print('数字人内核已启动')
    asyncio.run(main())
    # producer_task  = asyncio.get_event_loop().run_until_complete(producer(queue))

    # close_connection()
