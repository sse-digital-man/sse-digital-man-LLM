import sys

sys.path.append('.')

import time
import math
import csv

from text2vec import SentenceModel
from config.ConfigLoader import config
from core.db_operate.connection_handler import get_db_client
# from chromadb import EmbeddingFunction, Documents, Embeddings

# class MyEmbeddingFunction(EmbeddingFunction):
#     def __call__(self, input: Documents) -> Embeddings:
#         embedder = SentenceModel("shibing624/text2vec-base-chinese")
#         embeddings = embedder.encode(input)
#
#         # 转化为单位向量
#         for vec in embeddings:
#             vec_len = 0
#             for x in vec:
#                 vec_len = vec_len + x ** 2
#
#             vec_len = math.sqrt(vec_len)
#
#             for i in range(len(vec)):
#                 vec[i] = vec[i] / vec_len
#
#         return embeddings


class DbOperator:
    def __init__(self):
        self.embedder = SentenceModel("shibing624/text2vec-base-chinese")
        self.client = get_db_client()

    def create_collection(self, collection_name):
        collection = self.client.create_collection(name=collection_name)

        print("collection created")

        return collection

    def search(self, collection_name, search_text):
        search_start_time = time.time()

        # get collection
        collection = self.client.get_collection(collection_name)

        # get query embedding
        query_embedding = self.embedder.encode(search_text)

        # conduct query
        results = collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=config.db_k
        )

        search_end_time = time.time()

        search_elapsed_time = search_end_time - search_start_time

        # print used time
        print(f"[info] 信息检索完毕。检索用时{format(search_elapsed_time, '.2f')}s")

        # print result
        search_result = []

        for idx, similarity in zip(results['ids'][0], results['distances'][0]):
            search_result.append((idx, similarity))

        return search_result

    def create_embeddings(self, collection_name):
        # get collection
        collection = self.client.get_collection(collection_name)

        # read the keyword column in the csv file
        keyword_list = []
        with open("data.csv", newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader, None)  # 跳过首行
            for row in reader:
                keyword_list.append(row[0])

        # calculate vectors
        embeddings = self.embedder.encode(keyword_list)

        # 转化为单位向量
        for vec in embeddings:
            vec_len = 0
            for x in vec:
                vec_len = vec_len + x ** 2

            vec_len = math.sqrt(vec_len)

            for i in range(len(vec)):
                vec[i] = vec[i] / vec_len


        # save embeddings in the collection
        collection.add(
            documents=keyword_list,
            ids=[str(i) for i in range(0, len(keyword_list))],
            embeddings=embeddings.tolist()
        )

        print("embeddings created, embedding count: " + str(len(keyword_list)))

db_operator = DbOperator()