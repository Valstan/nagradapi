from pydantic import BaseModel


class Persons(BaseModel):
    name: str = None
    family: str = None
    avatar: str = None
    birthdate: int = None
    phone: str = None
    email: str = None
    login: str = None
    password: str = None
    theme: str = None
    token: str = None


class GreatPerson(Persons):
    login: str
    password: str
    token_date: int = None


class GetPersons(BaseModel):
    token: str
    field_key: str
    field_value: str


class UpdateToken(BaseModel):
    login: str
    password: str


class GetData(BaseModel):
    token: str
    id: str
