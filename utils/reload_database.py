import sys

sys.path.append(".")

from config import db_config
from core.db_operate.DB_Operator import DbOperator
from utils.drop_database import drop_database


# 重新执行create_collection和create_embeddings

def reload_database(collection_name):
    db_operator = DbOperator()
    # if collection with the same name already exists, drop the original collection
    drop_database(collection_name)
    # create collection
    db_operator.create_collection(collection_name)
    # create embeddings
    db_operator.create_embeddings(collection_name)

if __name__ == '__main__':
    reload_database(db_config.COLLECTION_NAME)
