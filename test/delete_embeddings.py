from pymilvus import connections, Collection
from config import db_config

# connect to milvus server
connections.connect(
    alias="default",
    user="",
    password="",
    host="localhost",
    port='19530'
)

# get collection
collection = Collection(db_config.COLLECTION_NAME)

# load collection
collection.load()

# get embedding vector count
print(collection.num_entities)

# delete all embeddings
collection.delete("id in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]")
collection.flush()

# get embedding vector count
print(collection.num_entities)
