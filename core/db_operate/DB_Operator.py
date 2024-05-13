import sys
sys.path.append("")

import time
import math
import csv
from pymilvus import FieldSchema, CollectionSchema, Collection, DataType, connections, utility
from text2vec import SentenceModel
from config import db_config
from core.db_operate.connection_handler import open_connection, close_connection

class DbOperator:
    def __init__(self):
        self.embedder = SentenceModel("shibing624/text2vec-base-chinese")
        self.k = 5
        self.DIM = 768
        self.collection_name = "digital_man_text2vec"

    def create_collection(self, collection_name):
        id = FieldSchema(
            name="id",
            dtype=DataType.INT64,
            is_primary=True
        )
        emb = FieldSchema(
            name="emb",
            dtype=DataType.FLOAT_VECTOR,
            dim=self.DIM
        )

        schema = CollectionSchema(
            fields=[id, emb],
            enable_dynamic_field=True
        )

        collection = Collection(
            name=collection_name,
            schema=schema,
            using='default',
            shards_num=2,
            consistency_level="Strong"
        )

        collection.flush()

        print("collection created")

        return collection

    def search(self, search_text):
        open_connection()

        keyword_list = []
        with open("data.csv", newline='') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader, None)  # 跳过首行
            for row in reader:
                keyword_list.append(row[0])

        # create target embedding
        embed_start_time = time.time()

        emb_target = self.embedder.encode(search_text)
        # 转换为单位向量
        vec_len = 0
        for x in emb_target:
            vec_len = vec_len + x ** 2

        vec_len = math.sqrt(vec_len)

        for i in range(len(emb_target)):
            emb_target[i] = emb_target[i] / vec_len

        embed_end_time = time.time()
        embed_elapsed_time = embed_end_time - embed_start_time

        # load collection to memory
        collection = Collection(db_config.COLLECTION_NAME)
        collection.load()

        # conduct similarity search

        search_start_time = time.time()

        search_params = {
            "metric_type": "IP",
            "offset": 0,
            "ignore_growing": False,
            "params": {"nprobe": 10}
        }

        results = collection.search(
            data=[emb_target],
            anns_field="emb",
            param=search_params,
            limit=self.k,
            expr=None,
            output_fields=['output'],
            consistency_level="Strong"
        )

        search_end_time = time.time()
        search_elapsed_time = search_end_time - search_start_time

        # print used time and search result
        print(
            f"[info] 信息检索完毕。embed用时{format(embed_elapsed_time, '.2f')}s，检索用时{format(search_elapsed_time, '.2f')}s")

        # return result
        hits = results[0]
        search_result = []
        for idx, similarity in zip(hits.ids, hits.distances):
            search_result.append((idx, similarity))

        close_connection()

        return search_result

    def create_embeddings(self, collection_name):
        # get collection
        collection = Collection(collection_name)

        # read the keyword column in the csv file
        keyword_list = []
        with open("data.csv", newline='') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader, None)  # 跳过首行
            for row in reader:
                keyword_list.append(row[0])

        # create embeddings
        emb_list = self.embedder.encode(keyword_list)

        # 转化为单位向量
        for vec in emb_list:
            vec_len = 0
            for x in vec:
                vec_len = vec_len + x ** 2

            vec_len = math.sqrt(vec_len)

            for i in range(len(vec)):
                vec[i] = vec[i] / vec_len

        # 输出第一个embedding向量的长度，检查一下
        # first_vec_len = 0
        # for x in emb_list[0]:
        #     first_vec_len = first_vec_len + x ** 2
        # first_vec_len = math.sqrt(first_vec_len)
        # print(f"first_vec_len={first_vec_len}")

        # build an index
        index_params = {
            "metric_type": "IP",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128}
        }

        collection.create_index(
            field_name="emb",
            index_params=index_params,
            index_name="MyIndex"
        )

        # print("index built")
        utility.index_building_progress(collection_name)

        # load collection, save embeddings to it
        data = [[i for i in range(len(emb_list))], emb_list]

        collection.insert(data)

        collection.flush()

        print("embeddings created in milvus database, embedding count: " + str(len(emb_list)))

        # release collection, disconnect
        connections.disconnect("default")