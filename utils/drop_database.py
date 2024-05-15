import sys

sys.path.append(".")
from core.db_operate.connection_handler import get_db_client
from config import db_config

def drop_database(collection_name):
    client = get_db_client()

    collections = client.list_collections()

    if collection_name in [c.name for c in collections]:
        client.delete_collection(collection_name)

if __name__ == '__main__':
    drop_database(db_config.COLLECTION_NAME)
