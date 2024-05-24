import sys

sys.path.append(".")

from config.ConfigLoader import config
from core.db_operate.DB_Operator import DbOperator
from utils.drop_database import drop_database


def reload_database(collection_name):
    db_operator = DbOperator()
    # if collection with the same name already exists, drop the original collection
    drop_database(collection_name)
    # create collection
    db_operator.create_collection(collection_name)
    # create embeddings
    db_operator.create_embeddings(collection_name)

if __name__ == '__main__':
    reload_database(config.db_collection_name)
