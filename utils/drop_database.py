import sys

sys.path.append(".")

from config import db_config
from pymilvus import utility

from db_operate.connection_handler import open_connection
from db_operate.connection_handler import close_connection


def drop_database():
    # if collection with the same name already exists, drop the original collection
    if utility.has_collection(db_config.COLLECTION_NAME):
        utility.drop_collection(db_config.COLLECTION_NAME)
        print("original collection dropped")

open_connection()
drop_database()
close_connection()
