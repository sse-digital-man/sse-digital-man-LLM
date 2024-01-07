from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility

DIM = 768 #向量维数。这是一个常量，由Embedding model决定
collection_name = "digital_man_text2vec"

#connect to milvus server
connections.connect(
    alias="default",
    user="",
    password="",
    host="localhost",
    port='19530'
)

#if collection with the same name already exists, delete the original collection
if utility.has_collection(collection_name):
    utility.drop_collection(collection_name)
    print("original collection deleted")

#create collection
id = FieldSchema(
    name = "id",
    dtype=DataType.INT64,
    is_primary=True
)
emb = FieldSchema(
    name = "emb",
    dtype=DataType.FLOAT_VECTOR,
    dim=DIM
)

schema = CollectionSchema(
    fields=[id, emb],
    enable_dynamic_field=True #
)

collection = Collection(
    name = collection_name,
    schema=schema,
    using='default',
    shards_num=2,
    consistency_level="Strong"
)

print("Collection created")