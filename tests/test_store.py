import allure
import requests
import jsonschema
import pytest

from .conftest import create_order
from .schemas.order_schema import ORDER_SCHEMA
from .schemas.inventory_schema import INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_add_new_order(self, create_order):
        with allure.step("Подготовка данных для создания заказа"):
            payload = create_order  # данные берутся из фикстуры

        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схеме"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, ORDER_SCHEMA)

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json['id'] == payload['id'], "id заказа не совпадает с ожидаемым"
            assert response_json['petId'] == payload['petId'], "id питомца не совпадает с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "количество питомцев не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "статус не совпадает с ожидаемым"


    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_order):
        with allure.step("Получение ID размещенного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Ответ содержит данные с id заказа"):
            assert response.json()["id"] == order_id, "id заказа не совпал с ожидаемым"


    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Получение ID размещенного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на удаление информации о заказе по ID"):
            response = requests.delete(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации об удаленном заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Order not found", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Order not found", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step(f"Отправка запроса на получение инвентаря"):
            response = requests.get(f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка на тип объекта в ответе"):
            assert isinstance(response.json(), dict), "Тип объекта не совпал с ожидаемым"

        with allure.step("Проверка валидации JSON-схеме"):
            jsonschema.validate(response.json(), INVENTORY_SCHEMA), "Значение не является целым числом integer($int32)"