import sys

sys.path.append(".")

from config import db_config
from core.db_operate.DB_Operator import DbOperator
from core.db_operate.connection_handler import open_connection
from core.db_operate.connection_handler import close_connection
from core.db_operate.create_embeddings import create_embeddings
from utils.drop_database import drop_database


# 重新执行create_collection和create_embeddings

def reload_database():
    db_operator = DbOperator()
    # if collection with the same name already exists, drop the original collection
    drop_database()
    # create collection
    db_operator.create_collection(db_config.COLLECTION_NAME)
    # create embeddings
    db_operator.create_embeddings(db_config.COLLECTION_NAME)

open_connection()
reload_database()
close_connection()
