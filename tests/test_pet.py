from types import NoneType

import allure
import requests
import jsonschema
import pytest
from .schemas.pet_schema import PET_SCHEMA
from requests.exceptions import JSONDecodeError

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Попытка обновить несуществующего питомца")
    def test_put_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {"id": 9999,
                       "name": "Non-existent Pet",
                       "status": "available"}
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {"id": 1,
                       "name": "Buddy",
                       "status": "available"
                       }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схеме"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id']==payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name']==payload['name'], "имя питомца не совпадает с ожидаемым"
            assert response_json['status']==payload['status'], "статус не совпадает с ожидаемым"


    @allure.title("Добавление нового питомца c полными данными")
    def test_add_full_pet(self):
        with allure.step("Подготовка данных для создания питомца с полными данными"):
            payload = {"id": 10,
                       "name": "doggie",
                       "category": {
                           "id": 1,
                           "name": "Dogs"
                       },
                       "photoUrls": [
                           "string"
                       ],
                       "tags": [
                           {"id": 0,
                            "name": "string"
                            }
                       ],
                       "status": "available"
                       }

        with allure.step("Отправка запроса на создание питомца с полными данными"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схеме"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id']==payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name']==payload['name'], "имя питомца не совпадает с ожидаемым"
            assert response_json['status']==payload['status'], "статус не совпадает с ожидаемым"


    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id


    @allure.title("Обновление информации о питомце")
    def test_update_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для обновления питомца"):
            payload = {"id": create_pet["id"],
                       "name": "Buddy Updated",
                       "status": "sold"
                       }

        with allure.step("Отправка запроса на обновление питомца"):
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id']==payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name']==payload['name'], "имя питомца не совпадает с ожидаемым"
            assert response_json['status']==payload['status'], "статус не совпадает с ожидаемым"



    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

        with allure.step("Удаление питомца по ID"):
            response = requests.delete(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"


# Урок 5. Параметризованные тесты
    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize( # В методе передаем строку с именами параметров (status, expected_status_code, is_json_response, expected_type) и список значений — каждый элемент списка — это кортеж (tuple)
        "status, expected_status_code, is_json_response, expected_type", # Параметры is_json_response и expected_type нужны, чтобы обработать ошибки при негативных кейсах: при несуществующем или пустом значении статуса сервер возвращает json с объектом ошибки с code и message (dict), а не список (list). А при отсутствии статуса (None) сервер не возвращает JSON.
        [
            ("available", 200, True, list), # в ответе придет список (list)
            ("pending", 200, True, list),
            ("sold", 200, True, list),
            ("vdvd", 400, True, dict), # недопустимый статус, в ответе придет JSON-объект ошибки с словарем (dict), а не список (list): {"code": 400,"message": "Input error: query parameter `status` value `vdvd` is not in the allowable values `[available, pending, sold]`"}
            ("", 400, True, dict), # пустой статус, в ответе придет JSON-объект ошибки с словарем (dict), а не список (list): {"code": 400,"message": "Input error: query parameter `status` value `` is not in the allowable values `[available, pending, sold]`"}
            (None, 400, False, None) # отсутствующий параметр, в ответе не-JSON (ожидается JSONDecodeError).
        ]
    )
    def test_get_pets_by_status(self, status, expected_status_code, is_json_response, expected_type):
        with allure.step(f"Отправка запроса на получение питомцев по статусу {status}"):
            params = {"status": status} if status is not None else {}
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params=params)

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code

            if is_json_response:
                assert isinstance(response.json(), expected_type)
            else:
                # Когда JSON НЕ парсится, падаем с исключением JSONDecodeError
                with pytest.raises(requests.exceptions.JSONDecodeError): # pytest.raises(...)-cпециальный инструмент в фреймворке pytest, который ожидает, что внутри блока with будет вызвано указанное исключение. requests.exceptions.JSONDecodeError-тип исключения. Возникает, когда метод response.json() пытается распарсить строку, которая не является валидным JSON (неправильные кавычки, отсутствуют скобки, неверная структура)
                    response.json()