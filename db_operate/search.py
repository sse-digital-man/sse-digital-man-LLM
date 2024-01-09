import sys
sys.path.append(".")

import time
import math
import csv
from pymilvus import Collection
from text2vec import SentenceModel
import config

def search(search_text):
    embedder = SentenceModel("shibing624/text2vec-base-chinese")
    k = 5

    keyword_list = []
    with open("data.csv", newline='') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader, None)  # 跳过首行
        for row in reader:
            keyword_list.append(row[0])

    start_time = time.time()
    # create target embedding
    emb_target = embedder.encode(search_text)
    # 转换为单位向量
    vec_len = 0
    for x in emb_target:
        vec_len = vec_len + x ** 2

    vec_len = math.sqrt(vec_len)

    for i in range(len(emb_target)):
        emb_target[i] = emb_target[i] / vec_len

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"对query进行embedding耗时：{elapsed_time}秒")

    # load collection to memory
    collection = Collection(config.COLLECTION_NAME)
    collection.load()

    # conduct similarity search

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

    # return result
    hits = results[0]
    search_result = []
    for idx, similarity in zip(hits.ids, hits.distances):
        search_result.append((idx, similarity))

    return search_result