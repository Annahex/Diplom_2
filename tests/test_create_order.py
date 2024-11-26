import requests
import allure
from urls.urls import CREATE_ORDER_URL
import pytest


MESSAGE_NO_INGREDIENTS = "Ingredient ids must be provided"


class TestCreateOrder:

    @allure.title('Проверка создания заказа с авторизацией и без')
    @pytest.mark.parametrize('need_auth', [True, False])
    def test_can_create_order(self, user, random_ingredients, need_auth):
        payload = {
            "ingredients": random_ingredients
        }
        headers = {"Authorization": user['accessToken']} if need_auth else {}
        response = requests.post(CREATE_ORDER_URL, data=payload, headers=headers)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert len(body["name"]) > 0
        assert body["order"]["number"] > 0

    @allure.title('Проверка создания заказа с авторизацией, но без ингредиентов')
    def test_cant_create_order_without_ingredients(self, user):
        payload = {
            "ingredients": []
        }
        response = requests.post(CREATE_ORDER_URL, data=payload, headers={"Authorization": user['accessToken']})
        body = response.json()

        assert response.status_code == 400
        assert body["success"] is False
        assert body["message"] == MESSAGE_NO_INGREDIENTS

    @allure.title('Проверка создания заказа с неверными ингредиентами')
    def test_cant_create_order_without_ingredients(self, user):
        payload = {
            "ingredients": ["wrong", "ingredient"]
        }
        response = requests.post(CREATE_ORDER_URL, data=payload, headers={"Authorization": user['accessToken']})

        assert response.status_code == 500


