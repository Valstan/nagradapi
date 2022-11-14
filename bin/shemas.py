from pydantic import BaseModel


class Persons(BaseModel):
    name: str = None
    family: str = None
    login: str = None
    password: str = None
    avatar: str = None
    phone: str = None
    email: str = None
    telegram: str = None
    theme: str = None
    token: str = None


class GreatPerson(Persons):
    login: str
    password: str


class GetPersons(BaseModel):
    token: str
    field_key: str
    field_value: str


class UpdateToken(BaseModel):
    login: str
    password: str


class GetDataSets(BaseModel):
    token: str


class PutDataSets(BaseModel):
    token: str
    collection: str
    data: dict = {}
