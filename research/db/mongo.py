from core.config import settings

from pymongo import MongoClient


def create_connect_mongo():
    client = MongoClient(settings.mongo_host, settings.mongo_port)
    db = client[settings.mongo_base]
    return db
