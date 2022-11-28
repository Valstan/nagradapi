import hashlib
import time

from uuid6 import uuid7

from fastapi import FastAPI

from bin.get_mongo_base import base
from bin.token_lifetime import token_lifetime
from bin.shemas import Persons, GetPersons, UpdateToken, GreatPerson, GetDataSets, PutDataSets

app = FastAPI()


# Не зашифрованы в базе лишь день рождения и case и currency
@app.post('/nagrada/get_persons')
def get_persons(item: GetPersons):
    collection = base['persons']
    table = collection.find_one({'token': hashlib.sha256(item.token.encode()).hexdigest()},
                                {"_id": 1, "token_date": 1})
    if table \
            and token_lifetime(table['token_date']) \
            and str(table['_id']) == '637009dda9bfdba38e6f0094':
        persons_list = collection.find({item.field_key: hashlib.sha256(item.field_value.encode()).hexdigest()})
        persons_list = [Persons(**r) for r in persons_list]
        if persons_list:
            return persons_list
        return "nothing found"
    return "wrong token"


@app.post('/nagrada/update_person')
def update_person(item: Persons):
    collection = base['persons']
    table = collection.find_one({'token': hashlib.sha256(item.token.encode()).hexdigest()},
                                {"_id": 1, "token_date": 1})
    if table and token_lifetime(table['token_date']):
        item.token = None
        dic = {k: hashlib.sha256(v.encode()).hexdigest() for k, v in item.dict().items() if v is not None}
        collection.update_one({'_id': table['_id']},
                              {'$set': dic},
                              upsert=True)
        return "ok"
    return "wrong token"


@app.post('/nagrada/update_token')
def update_token(item: UpdateToken):
    item.login = hashlib.sha256(item.login.encode()).hexdigest()
    item.password = hashlib.sha256(item.password.encode()).hexdigest()
    collection = base['persons']
    table = collection.find_one({'login': item.login, 'password': item.password},
                                {"_id": 1})
    if table:
        token = str(uuid7())
        collection.update_one(table,
                              {'$set': {'token': hashlib.sha256(token.encode()).hexdigest(),
                                        'token_date': int(time.time())}},
                              upsert=True)
        return token
    return "no login or bad password"


@app.post('/nagrada/great_person')
def great_person(item: GreatPerson):
    item = {k: v for k, v in item.dict().items() if v is not None}
    collection = base['persons']
    table = collection.find_one({'login': hashlib.sha256(item['login'].encode()).hexdigest()}, {"id": 1})

    if table:
        return "login is busy"

    token = str(uuid7())
    item = {k: hashlib.sha256(v.encode()).hexdigest() for k, v in item.items()}
    item['token_date'] = int(time.time())
    item['token'] = hashlib.sha256(token.encode()).hexdigest()
    collection.update_one({'token': item['token']},
                          {'$set': item},
                          upsert=True)
    table = collection.find_one({'token': item['token']}, {"_id": 1})
    collection = base['data']
    collection.update_one(table,
                          {'$set': {str(int(time.time())): {'$set': collection.find_one({'id': 'data'}, {'0': 1})}}},
                          upsert=True)
    collection = base['sets']
    collection.update_one(table,
                          {'$set': collection.find_one({'id': 'sets'}, {'_id': 0, 'id': 0})},
                          upsert=True)
    return token


@app.post('/nagrada/get_data_sets')
def get_data_sets(item: GetDataSets):
    token = hashlib.sha256(item.token.encode()).hexdigest()
    collection = base['persons']
    table = collection.find_one({'token': token}, {"_id": 1, "token_date": 1})
    if table and token_lifetime(table['token_date']):
        collection = base[item.collection]
        table = collection.find_one({'_id': table['_id']}, {'_id': 0})
        return table
    return "wrong token"


@app.post('/nagrada/put_data_sets')
def put_data_sets(item: PutDataSets):
    item = item.dict()
    collection = base['persons']
    table = collection.find_one({'token': hashlib.sha256(item['token'].encode()).hexdigest()},
                                {"_id": 1, "token_date": 1})
    if table and token_lifetime(table['token_date']):
        collection = base[item['collection']]
        collection.update_one({'_id': table['_id']},
                              {'$set': item['data']},
                              upsert=True)
        return "ok"
    return "wrong token"
