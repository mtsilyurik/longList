from faker import Faker
from dataclasses import dataclass
from pprint import pprint
from random import choice
import json
import requests
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

@dataclass
class Product:
    categoryId: str
    name: str
    description: str
    price: int


BASE_URL = "http://localhost:2424"
URL = {
    "register": BASE_URL + "/auth/register",
    "login": BASE_URL + "/auth/login",
    "create_product": BASE_URL + "/product/create",
    "get_all_users": BASE_URL + "/user/get-all",
}

HEADERS = {"Content-Type": "application/json"}

generate = Faker()
admin = User(
    email="super@gmail.com",
    password="password",
    name="admin",
    phoneNumber="+123456789"
)

def register(u: User):
    payload = json.dumps(u.__dict__)
    response = requests.post(url=URL.get("register"), headers=HEADERS, data=payload)

    print(response.status_code)

    if response.status_code == 500:
        print(response.text)

def loginAdmin() -> dict:
    payload = json.dumps(admin.__dict__)
    response = requests.post(url=URL.get("login"), headers=HEADERS, data=payload)
    if response.status_code == 500:
        print(response.text)

    response = json.loads(response.text)
    token = response["token"]

    header ={"Authorization": "Bearer " + token}

    return header

def login(u: User) -> dict:
    payload = json.dumps(u.__dict__)
    response = requests.post(url=URL.get("login"), headers=HEADERS, data=payload)
    if response.status_code != 200:
        print(response.text)

    response = json.loads(response.text)
    token = response["token"]

    header = {"Authorization": "Bearer " + token,
              "Content-Type": "application/json"}

    return header

def createProduct(headers: dict) -> int:
    p = Product(
        categoryId="1",
        name=generate.word(),
        description=generate.sentence(),
        price=generate.random_number(),
    )

    payload = json.dumps(p.__dict__)
    print(payload)
    headers["Content-Type"] = "multipart/form-data; boundary=<calculated when request is sent>"
    response = requests.post(url=URL.get("create_product"), headers=headers, data=payload)

    if response.status_code != 200:
        print(response.text)

    return response.status_code

def get_all_users() -> (int, list):
    headers = loginAdmin()
    print(headers)
    response = requests.get(url=URL.get("get_all_users"), headers=headers)
    if response.status_code != 200:
        print(response.text)
        return response.status_code, []

    users = json.loads(response.text).get("userList")

    return response.status_code, users



def main():
    code, users = get_all_users()
    print(code)
    print(users)


if __name__ == "__main__":
    main()
