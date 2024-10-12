from faker import Faker
from dataclasses import dataclass
from pprint import pprint
import json

import requests

URL = "http://localhost:2424/auth/register"
HEADERS = {"Content-Type": "application/json"}
gen = Faker()


@dataclass
class User:
    email: str
    name: str
    password: str
    phoneNumber: str


@dataclass
class category:
    id: int
    name: str
    description: str
    price: int
    image: str


def register(u: User):
    payload = json.dumps(u.__dict__)
    response = requests.post(url=URL, headers=HEADERS, data=payload)

    print(response.status_code, end=" ")
    if response.status_code == 500:
        print(response.text)


for _ in range(5):
    print(_, end=" ")
    user = User(email=gen.email(), name=gen.name(), password=gen.password(), phoneNumber=gen.phone_number())
    register(user)
