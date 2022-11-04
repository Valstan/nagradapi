from pymongo import MongoClient

import config

client = MongoClient(config.MONGO_URI)
nagrada_base = client[config.base_name]
