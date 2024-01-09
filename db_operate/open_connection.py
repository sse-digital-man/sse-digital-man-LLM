from pymilvus import connections


def open_connection():
    connections.connect(
        alias="default",
        user="",
        password="",
        host="localhost",
        port='19530'
    )
