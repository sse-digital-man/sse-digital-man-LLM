import sys

sys.path.append(".")

from config import db_config

from core.db_operate.connection_handler import open_connection
from core.db_operate.connection_handler import close_connection
from core.db_operate.create_collection import create_collection
from core.db_operate.create_embeddings import create_embeddings
from utils.drop_database import drop_database


# 重新执行create_collection和create_embeddings

def reload_database():
    # if collection with the same name already exists, drop the original collection
    drop_database()
    # create collection
    create_collection(db_config.COLLECTION_NAME)
    # create embeddings
    create_embeddings(db_config.COLLECTION_NAME)

open_connection()
reload_database()
close_connection()
