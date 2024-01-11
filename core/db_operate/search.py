import sys
sys.path.append("")

import time
import math
import csv
from pymilvus import Collection
from text2vec import SentenceModel
from config import db_config
from core.db_operate.connection_handler import open_connection, close_connection

def search(search_text):
    open_connection()

    embedder = SentenceModel("shibing624/text2vec-base-chinese")
    k = 5

    keyword_list = []
    with open("data.csv", newline='') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader, None)  # 跳过首行
        for row in reader:
            keyword_list.append(row[0])



    # create target embedding
    embed_start_time = time.time()

    emb_target = embedder.encode(search_text)
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
        limit=k,
        expr=None,
        output_fields=['output'],
        consistency_level="Strong"
    )

    search_end_time = time.time()
    search_elapsed_time = search_end_time - search_start_time

    # print used time and search result
    print(f"[info] 信息检索完毕。embed用时{format(embed_elapsed_time, '.2f')}s，检索用时{format(search_elapsed_time, '.2f')}s")

    # return result
    hits = results[0]
    search_result = []
    for idx, similarity in zip(hits.ids, hits.distances):
        search_result.append((idx, similarity))

    close_connection()

    return search_result