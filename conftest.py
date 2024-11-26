import requests
import pytest
from faker import Faker
from urls.urls import CREATE_USER_URL


@pytest.fixture()
def user():
    fake = Faker("ru_RU")
    payload = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    requests.post(CREATE_USER_URL, data=payload)
    return payload
