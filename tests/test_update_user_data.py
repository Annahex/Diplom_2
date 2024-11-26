import requests
import allure
from faker import Faker
from urls.urls import USER_INFO_URL
import pytest


MESSAGE_USER_UNAUTHORIZED = "You should be authorised"


class TestUpdateUserData:

    fake = Faker("ru_RU")

    update_data = [
        ("email", fake.email()),
        ("name", fake.name()),
        ("password", fake.password())
    ]

    @allure.title('Проверка изменения данных пользователя с авторизацией')
    @pytest.mark.parametrize('update_data', update_data)
    def test_can_update_user_data(self, user, update_data):
        payload = {
            f"{update_data[0]}": update_data[1]
        }
        response = requests.patch(USER_INFO_URL, data=payload, headers={"Authorization": user['accessToken']})
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        if update_data[0] != "password":
            assert body["user"][update_data[0]] == update_data[1]

    @allure.title('Проверка изменения данных пользователя без авторизации')
    @pytest.mark.parametrize('update_data', update_data)
    def test_cant_update_user_data(self, user, update_data):
        payload = {
            f"{update_data[0]}": update_data[1]
        }
        response = requests.patch(USER_INFO_URL, data=payload)
        body = response.json()

        assert response.status_code == 401
        assert body["success"] is False
        assert body["message"] == MESSAGE_USER_UNAUTHORIZED
