import requests
import allure
from faker import Faker
from urls.urls import CREATE_USER_URL
import pytest


MESSAGE_USER_ALREADY_EXISTS = "User already exists"
MESSAGE_REQUIRED_FIELDS = "Email, password and name are required fields"


class TestCreateUser:

    payload = [
        {
            "email": "test@email.com",
            "password": "password"
        },
        {
            "email": "test@email.com",
            "name": "John Doe"
        },
        {
            "password": "password",
            "name": "John Doe"
        }
    ]

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
    @pytest.mark.parametrize('payload', payload)
    def test_cant_create_user_without_any_field(self, payload):
        response = requests.post(CREATE_USER_URL, data=payload)
        body = response.json()

        assert response.status_code == 403
        assert body["success"] is False
        assert body["message"] == MESSAGE_REQUIRED_FIELDS
