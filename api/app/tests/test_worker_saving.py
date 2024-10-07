import os
import django
import unittest
from unittest.mock import patch
from django.test import Client

from src.base_crud import BaseCRUD


class MockBaseCRUD(BaseCRUD):
    def commit(self):
        pass


class TestWorkerSaving(unittest.TestCase):

    @patch('src.base_crud.BaseCRUD')
    def test_correct_saving_from_service_1(self, MockBaseCRUD):
        data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "patronymic": "patronymic",
            "phone": ["+7-900-111-11-11"],
            "status": "1",
            "category": "courier"
        }
        c = Client()
        response = c.post('/api/v1/service1/', data)
        self.assertEqual(response.status_code, 200)

    @patch('src.base_crud.BaseCRUD')
    def test_correct_saving_from_service_2(self, MockBaseCRUD):
        data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "patronymic": "patronymic",
            "phone": ["+7-900-111-11-11", "+7-900-222-22-22"],
            "status": 3
        }
        c = Client()
        response = c.post('/api/v1/service2/', data)
        self.assertEqual(response.status_code, 200)

    @patch('src.base_crud.BaseCRUD')
    def test_correct_saving_from_service_3(self, MockBaseCRUD):
        data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "patronymic": "patronymic",
            "phone": ["+7-900-111-11-11", "+7-900-222-22-22"],
            "document": "34567"
        }
        c = Client()
        response = c.post('/api/v1/service3/', data)
        self.assertEqual(response.status_code, 200)

    @patch('src.base_crud.BaseCRUD')
    def test_correct_saving_from_service_4(self, MockBaseCRUD):
        data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "patronymic": "patronymic",
            "phone": ["+7-900-111-11-11", "89002221111"],
        }
        c = Client()
        response = c.post('/api/v1/service4/', data)
        self.assertEqual(response.status_code, 200)

    @patch('src.base_crud.BaseCRUD')
    def test_wrong_saving_telephone(self, MockBaseCRUD):
        data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "patronymic": "patronymic",
            "phone": ["8900111111a"],
        }
        c = Client()
        response = c.post('/api/v1/service4/', data)
        self.assertEqual(response.status_code, 400)

    @patch('src.base_crud.BaseCRUD')
    def test_wrong_saving_status(self, MockBaseCRUD):
        data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "patronymic": "patronymic",
            "phone": ["+7-900-111-11-11", "+7-900-222-22-22"],
            "status": 33
        }
        c = Client()
        response = c.post('/api/v1/service2/', data)
        self.assertEqual(response.status_code, 400)

    @patch('src.base_crud.BaseCRUD')
    def test_wrong_saving_category(self, MockBaseCRUD):
        data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "patronymic": "patronymic",
            "phone": ["+7-900-111-11-11"],
            "status": "1",
            "category": "courier2"
        }
        c = Client()
        response = c.post('/api/v1/service1/', data)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'src.config.settings')
    django.setup()
    unittest.main()
