from pymilvus import Collection, CollectionSchema, FieldSchema, DataType

DIM = 768  # 向量维数。这是一个常量，由Embedding model决定


def create_collection(collection_name):
    id = FieldSchema(
        name="id",
        dtype=DataType.INT64,
        is_primary=True
    )
    emb = FieldSchema(
        name="emb",
        dtype=DataType.FLOAT_VECTOR,
        dim=DIM
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
