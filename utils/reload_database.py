import sys
sys.path.append(".")

from config import db_config
from pymilvus import utility
from db_operate.open_connection import open_connection
from db_operate.create_collection import create_collection
from db_operate.create_embeddings import create_embeddings



# 重新执行create_collection和create_embeddings

open_connection()

# if collection with the same name already exists, drop the original collection
if utility.has_collection(config.COLLECTION_NAME):
    utility.drop_collection(config.COLLECTION_NAME)
    print("original collection deleted")

# create collection
create_collection(config.COLLECTION_NAME)

# create embeddings
create_embeddings(config.COLLECTION_NAME)
