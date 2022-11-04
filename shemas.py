from pydantic import BaseModel
from datetime import date


class PersonsConfig(BaseModel):
    theme: str
    level: int


class Persons(BaseModel):
    name: str
    family: str
    avatar: str
    birthdate: date
    phone: int
    email: str
    password: str
    config: PersonsConfig
