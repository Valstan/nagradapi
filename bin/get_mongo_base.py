from pymongo import MongoClient

import config

client = MongoClient(config.MONGO_URI)
base = client[config.base_name_na]
