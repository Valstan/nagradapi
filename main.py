import hashlib
import time
# from random import randint

from uuid6 import uuid7

from fastapi import FastAPI

from bin.get_mongo_base import nagrada_base
from bin.token_lifetime import token_lifetime
from shemas import Persons, GetPersons, UpdateToken, GreatPerson, GetData

app = FastAPI()


@app.post('/nagrada/get_person')
def get_person(item: GetPersons):
    token = hashlib.sha256(item.token.encode()).hexdigest()
    collection = nagrada_base['persons']
    table = collection.find_one({'token': token}, {"id": 1, "token_date": 1})
    if table \
            and token_lifetime(table['token_date']) \
            and table['id'] == 1668023774:
        persons_list = collection.find({item.field_key: item.field_value}, {"_id": 0})
        return [Persons(**r) for r in persons_list]
    return "wrong token"


@app.post('/nagrada/update_person')
def update_person(item: Persons):
    token = hashlib.sha256(item.token.encode()).hexdigest()
    collection = nagrada_base['persons']
    table = collection.find_one({'token': token}, {"id": 1, "token_date": 1})
    if table and token_lifetime(table['token_date']):
        del table['token_date']
        item.token = None
        dic = {k: v for k, v in item.dict().items() if v is not None}
        collection.update_one(table,
                              {'$set': dic},
                              upsert=True)
        return "ok"
    return "wrong token"


@app.post('/nagrada/update_token')
def update_token(item: UpdateToken):
    item.login = hashlib.sha256(item.login.encode()).hexdigest()
    item.password = hashlib.sha256(item.password.encode()).hexdigest()
    collection = nagrada_base['persons']
    table = collection.find_one({'login': item.login, 'password': item.password},
                                {"id": 1})
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
    collection = nagrada_base['persons']
    table = collection.find_one({'login': hashlib.sha256(item['login'].encode()).hexdigest()}, {"id": 1})

    if table:
        return "login is busy"

    token = str(uuid7())
    item = {k: hashlib.sha256(v.encode()).hexdigest() for k, v in item.items()}
    item['token_date'] = int(time.time())
    item['token'] = hashlib.sha256(token.encode()).hexdigest()
    collection.update_one({'token': item['token']},
                          {'$set': item,
                           '$currentDate': {'lastModified': True}},
                          upsert=True)
    oid = collection.find_one({'token': item['token']}, {"_id": 1})
    collection = nagrada_base['data']
    collection.update_one(oid,
                          {'$set': {str(int(time.time())): [1, 5, 100, 1]},
                           '$currentDate': {'lastModified': True}},
                          upsert=True)
    collection = nagrada_base['sets']
    collection.update_one(oid,
                          {'$set': {"101": "Вымыл полы"},
                           '$currentDate': {'lastModified': True}},
                          upsert=True)
    return [str(oid['_id']), token]


def get_data(item: GetData):
    token = hashlib.sha256(item.token.encode()).hexdigest()
    collection = nagrada_base['persons']
    table = collection.find_one({'token': token}, {"id": 1, "token_date": 1})
    if table and token_lifetime(table['token_date']):

        collection = nagrada_base['data']
        table = collection.find_one({'id': item.id}, {"id": 1, "token_date": 1})
    else:
        return "wrong token"
