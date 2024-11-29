import requests
import pytest
from faker import Faker
from urls.urls import CREATE_USER_URL, INGREDIENTS_URL
from random import randrange


@pytest.fixture()
def user():
    fake = Faker("ru_RU")
    payload = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    response = requests.post(CREATE_USER_URL, data=payload)
    body = response.json()
    return {
        **payload,
        "accessToken": body["accessToken"],
        "refreshToken": body["refreshToken"],
    }


@pytest.fixture()
def random_ingredients():
    response = requests.get(INGREDIENTS_URL)
    ingredients = response.json()["data"]
    buns = list(filter(lambda ing: ing["type"] == "bun", ingredients))
    mains = list(filter(lambda ing: ing["type"] == "main", ingredients))
    sauces = list(filter(lambda ing: ing["type"] == "sauce", ingredients))
    return [buns[randrange(len(buns))]["_id"], mains[randrange(len(mains))]["_id"], sauces[randrange(len(sauces))]["_id"]]
