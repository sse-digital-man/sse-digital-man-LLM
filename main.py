import sys
sys.path.append(".")

from pymilvus import Collection, utility
from config import db_config
from db_operate.connection_handler import open_connection
from db_operate.connection_handler import close_connection
from db_operate.create_collection import create_collection
from db_operate.create_embeddings import create_embeddings
from db_operate.search import search
from llm_core.bot import Bot as Bot

if __name__ == '__main__':
    open_connection()

    # initialize

    if not utility.has_collection(db_config.COLLECTION_NAME): # 如果collection不存在,创建collection
        create_collection(db_config.COLLECTION_NAME)

    collection = Collection(db_config.COLLECTION_NAME)

    if collection.num_entities == 0: # 如果无embedding,创建embedding
        create_embeddings(db_config.COLLECTION_NAME)


    # search

    print("请输入:")
    while True:
        user_input = input()

        if user_input.startswith('in '):
            # 提取'in '后面的字符串
            question = user_input[3:]
            search_result = search(question)
            bot = Bot()
            answer = bot.answer(question, search_result)
            print(answer)
        elif user_input == 'exit':
            break
        else:
            print("无效命令，请重新输入")

    close_connection()