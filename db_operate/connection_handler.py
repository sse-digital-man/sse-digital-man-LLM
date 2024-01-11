from pymilvus import connections


def open_connection():
    connections.connect(
        alias="default",
        user="",
        password="",
        host="localhost",
        port='19530'
    )
    print("connection opened")


def close_connection():
    connections.disconnect("default")
    print("connection closed")
