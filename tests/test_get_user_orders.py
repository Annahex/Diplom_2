import requests
import allure
from urls.urls import USER_ORDER_URL, CREATE_ORDER_URL


MESSAGE_USER_UNAUTHORIZED = "You should be authorised"


class TestGetUserOrders:

    @allure.title('Проверка получения заказов пользователя с авторизацией')
    def test_can_update_user_data(self, user, random_ingredients):
        payload = {
            "ingredients": random_ingredients
        }
        requests.post(CREATE_ORDER_URL, data=payload, headers={"Authorization": user['accessToken']})
        response = requests.get(USER_ORDER_URL, headers={"Authorization": user['accessToken']})
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["total"] == 1
        assert body["totalToday"] == 1
        assert len(body["orders"]) == 1

    @allure.title('Проверка получения заказов пользователя без авторизации')
    def test_can_update_user_data(self, user, random_ingredients):
        payload = {
            "ingredients": random_ingredients
        }
        requests.post(CREATE_ORDER_URL, data=payload, headers={"Authorization": user['accessToken']})
        response = requests.get(USER_ORDER_URL)
        body = response.json()

        assert response.status_code == 401
        assert body["success"] is False
        assert body["message"] == MESSAGE_USER_UNAUTHORIZED
