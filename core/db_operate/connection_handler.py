import sys

sys.path.append('.')

import chromadb
from config.ConfigLoader import config


def get_db_client():
    client = chromadb.HttpClient(host='localhost', port=config.db_client_port)
    return client

# def open_connection():
#     connections.connect(
#         alias="default",
#         user="",
#         password="",
#         host="localhost",
#         port='19530'
#     )
#     # print("connection opened")
#
#
# def close_connection():
#     connections.disconnect("default")
#     # print("connection closed")
