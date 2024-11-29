import requests
import allure
from faker import Faker
from urls.urls import CREATE_USER_URL
import pytest
from data.constants import MESSAGE_USER_ALREADY_EXISTS, MESSAGE_REQUIRED_FIELDS
from data.mock import DATA_FOR_USER_CREATE


class TestCreateUser:

    @allure.title('Проверка создания уникального пользователя')
    def test_can_create_new_user(self):
        fake = Faker("ru_RU")
        payload = {
            "email": fake.email(),
            "password": fake.password(),
            "name": fake.name()
        }

        response = requests.post(CREATE_USER_URL, data=payload)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"]["email"] == payload["email"]
        assert body["user"]["name"] == payload["name"]

    @allure.title('Проверка наличия ошибки создания пользователя, который уже зарегистрирован')
    def test_cant_create_same_user(self, user):
        payload = {
            "email": user["email"],
            "password": user["password"],
            "name": user["name"]
        }

        response = requests.post(CREATE_USER_URL, data=payload)
        body = response.json()

        assert response.status_code == 403
        assert body["success"] is False
        assert body["message"] == MESSAGE_USER_ALREADY_EXISTS

    @allure.title('Проверка наличия ошибки создания пользователя, у которого не указаны все обязательные поля')
    @pytest.mark.parametrize('payload', DATA_FOR_USER_CREATE)
    def test_cant_create_user_without_any_field(self, payload):
        response = requests.post(CREATE_USER_URL, data=payload)
        body = response.json()

        assert response.status_code == 403
        assert body["success"] is False
        assert body["message"] == MESSAGE_REQUIRED_FIELDS
