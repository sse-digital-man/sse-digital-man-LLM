import csv
import math

from pymilvus import connections, Collection, utility
from text2vec import SentenceModel

embedder = SentenceModel("shibing624/text2vec-base-chinese")
collection_name = "digital_man_text2vec"

# connect to milvus server
connections.connect(
    alias="default",
    user="",
    password="",
    host="localhost",
    port='19530'
)

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
emb_list = embedder.encode(keyword_list)

# 转化为单位向量
for vec in emb_list:
    vec_len = 0
    for x in vec:
        vec_len = vec_len + x ** 2

    vec_len = math.sqrt(vec_len)

    for i in range(len(vec)):
        vec[i] = vec[i] / vec_len

# 输出第一个embedding向量的长度，检查一下
first_vec_len = 0
for x in emb_list[0]:
    first_vec_len = first_vec_len + x ** 2
first_vec_len = math.sqrt(first_vec_len)
print(f"first_vec_len={first_vec_len}")

print("embedding created, sentence count: " + str(len(emb_list)))

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

print("index built")
utility.index_building_progress(collection_name)

# if embeddings already exist, delete original embeddings
expr = "TRUE"
collection.delete(expr)

# load collection, save embeddings to it
data = [[i for i in range(len(emb_list))], emb_list]

collection.insert(data)

print("embeddings created in milvus database")

# release collection, disconnect
connections.disconnect("default")
