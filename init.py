from faker import Faker
from dataclasses import dataclass
from pprint import pprint
from random import choice
import json
import requests
from requests import Session


@dataclass
class User:
    email: str
    name: str
    password: str
    phoneNumber: str


@dataclass
class Category:
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
    "get_all_by_slice": BASE_URL + "/user/get-all-by-slice?pageNumber=",
}

HEADERS = {"Content-Type": "application/json"}

generate = Faker()
admin = User(
    email="super@gmail.com",
    password="password",
    name="admin",
    phoneNumber="+123456789"
)


def register(u: User) -> int:
    payload = json.dumps(u.__dict__)
    response = requests.post(url=URL.get("register"), headers=HEADERS, data=payload)

    if response.status_code != 200:
        print(response.text)

    return response.status_code


def loginAdmin() -> dict:
    payload = json.dumps(admin.__dict__)
    response = requests.post(url=URL.get("login"), headers=HEADERS, data=payload)
    if response.status_code == 500:
        print(response.text)

    response = json.loads(response.text)
    token = response["token"]

    header = {"Authorization": "Bearer " + token}

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


def create_product(headers: dict) -> int:
    p = Product(
        categoryId=str("1"),
        name=generate.word(),
        description=generate.sentence(),
        price=generate.random_number(),
    )
    param = json.dumps(p.__dict__)
    # print(type(param))
    # headers["Content-Type"] = "multipart/form-data; boundary=<calculated when request is sent>"
    with Session() as session:
        response = session.post(url=URL.get("create_product"), headers=headers, data=json.loads(param))

        if response.status_code != 200:
            pprint(response.json())

        # print(response.text)
        # print(response.status_code)
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


def get_users_by_slice(pn: int) -> (int, list, int, int):
    headers = loginAdmin()
    response = requests.get(url=URL.get("get_all_by_slice") + str(pn), headers=headers)
    response_json = json.loads(response.text)

    if response.status_code != 200:
        print(response.text)
        return response.status_code, []

    users = response_json.get("usersPage").get("content")
    total_elements = response_json.get("usersPage").get("totalElements")
    total_pages = response_json.get("usersPage").get("totalPages")

    return response.status_code, users, total_elements, total_pages


def main():
    # code, users, total_elements, total_pages = get_users_by_slice(0)
    # print("Status code – " + str(code))
    # print("Total elements – " + str(total_elements))
    # print("Total pages – " + str(total_pages))
    # pprint(users)
    headers = loginAdmin()
    for _ in range(500):
        code = create_product(headers)
        print(code)

if __name__ == "__main__":
    main()
