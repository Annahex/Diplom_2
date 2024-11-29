import requests
import allure
from urls.urls import USER_INFO_URL, LOGIN_URL
import pytest
from data.constants import MESSAGE_USER_UNAUTHORIZED
from data.mock import DATA_FOR_USER_UPDATE


class TestUpdateUserData:

    @allure.title('Проверка изменения данных пользователя с авторизацией')
    @pytest.mark.parametrize('update_data', DATA_FOR_USER_UPDATE)
    def test_can_update_user_data(self, user, update_data):
        payload = {
            f"{update_data[0]}": update_data[1]
        }
        response = requests.patch(USER_INFO_URL, data=payload, headers={"Authorization": user['accessToken']})
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"][update_data[0]] == update_data[1]

    @allure.title('Проверка изменения данных пользователя с авторизацией')
    def test_can_update_user_password(self, user):
        new_password = "new_password"
        payload = {
            "password": new_password
        }
        response = requests.patch(USER_INFO_URL, data=payload, headers={"Authorization": user['accessToken']})

        assert response.status_code == 200

        payload = {
            "email": user["email"],
            "password": new_password
        }

        response = requests.post(LOGIN_URL, data=payload)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"]["email"] == user["email"]
        assert body["user"]["name"] == user["name"]
        assert len(body["accessToken"]) > 0
        assert len(body["refreshToken"]) > 0

    @allure.title('Проверка изменения данных пользователя без авторизации')
    @pytest.mark.parametrize('update_data', DATA_FOR_USER_UPDATE)
    def test_cant_update_user_data(self, user, update_data):
        payload = {
            f"{update_data[0]}": update_data[1]
        }
        response = requests.patch(USER_INFO_URL, data=payload)
        body = response.json()

        assert response.status_code == 401
        assert body["success"] is False
        assert body["message"] == MESSAGE_USER_UNAUTHORIZED
