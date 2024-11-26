import requests
import allure
from urls.urls import LOGIN_URL


MESSAGE_INCORRECT_CREDENTIALS = "email or password are incorrect"


class TestUserLogin:

    @allure.title('Проверка логина существующего пользователя')
    def test_can_login_as_existing_user(self, user):
        payload = {
            "email": user["email"],
            "password": user["password"]
        }

        response = requests.post(LOGIN_URL, data=payload)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"]["email"] == user["email"]
        assert body["user"]["name"] == user["name"]
        assert len(body["accessToken"]) > 0
        assert len(body["refreshToken"]) > 0

    @allure.title('Проверка ошибки логина несуществующего пользователя')
    def test_cant_login_as_wrong_user(self, user):
        payload = {
            "email": user["email"] + "123",
            "password": user["password"] + "123"
        }

        response = requests.post(LOGIN_URL, data=payload)
        body = response.json()

        assert response.status_code == 401
        assert body["success"] is False
        assert body["message"] == MESSAGE_INCORRECT_CREDENTIALS

