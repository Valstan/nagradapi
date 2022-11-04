from fastapi import FastAPI, Query

from shemas import Persons

app = FastAPI()


@app.get('/')
def home():
    return {"key": "Привет!"}


@app.get('/{pk}')
def get_item(pk: int):
    return {"key": pk}


@app.post('/persons')
def persons(item: Persons):
    return item


@app.get('/sets')
def get_sets(item: str = Query(None)):
    return item
