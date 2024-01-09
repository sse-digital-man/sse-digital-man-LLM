import sys
sys.path.append(".")

from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, utility
from db_operate.open_connection import open_connection
from db_operate.create_collection import create_collection
from db_operate.create_embeddings import create_embeddings
from db_operate.search import search
from llm_core.answer import answer

if __name__ == '__main__':
    collection_name = "digital_man_text2vec"

    open_connection()

    # initialize

    if not utility.has_collection(collection_name): # 如果collection不存在,创建collection
        create_collection(collection_name)

    collection = Collection(collection_name)

    if collection.num_entities == 0: # 如果无embedding,创建embedding
        create_embeddings(collection_name)

    # search

    print("请输入:")
    while True:
        user_input = input()

        if user_input.startswith('in '):
            # 提取'in '后面的字符串
            data_input = user_input[3:]
            search_result = search(data_input)
            answer(search_result)
        elif user_input == 'exit':
            break
        else:
            print("无效命令，请重新输入")