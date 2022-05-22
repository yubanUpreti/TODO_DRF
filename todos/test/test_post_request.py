import datetime
from pathlib import Path

import pytz
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from .base import create_user, create_todo, delete_user


class RegisterTestCase(APITestCase):
    def setUp(self):
        self.url = reverse_lazy('todos:todo-urls-list')
        # '/todos/'
        self.signin_url = reverse('login')
        self.home_dir = Path(__file__).resolve().parent.parent

    def get_auth_token(self, email="client@test.com", password="Admin@123"):
        data = {
            "email": email,
            "password": password
        }
        tkn = self.client.post(self.signin_url, data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tkn.data['access'])

    def test_post_todo_valid_data(self, image_path=None):
        user = create_user()
        self.get_auth_token()
        data = {
            "name": "First Todo",
            "description": "Hello",
            "deadline": datetime.datetime.fromisoformat("2022-06-01 11:00").replace(tzinfo=pytz.utc),
            "image": SimpleUploadedFile(name='images/todo/test.png', content=open('todos/test/test.png', 'rb').read(),
                                        content_type='image/png')
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"message": "Todo created successfully"})
        delete_user(user)

    def test_post_todo_same_title(self):
        user, todo = create_todo()
        self.get_auth_token()
        data = {
            "name": "Test Todo",
            "description": "Hello",
            "deadline": datetime.datetime.fromisoformat("2022-06-01 11:00").replace(tzinfo=pytz.utc),
            "image": SimpleUploadedFile(name='test.png', content=open('todos/test/test.png', 'rb').read(),
                                        content_type='image/png')
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,
                         {"message": [ErrorDetail(string='Todo with this name already exists.', code='invalid')]})
        delete_user(user)

    def test_post_todo_past_date(self):
        user, todo = create_todo()
        self.get_auth_token()
        data = {
            "name": "Test Todo Updated",
            "description": "Hello",
            "deadline": datetime.datetime.fromisoformat("2022-01-01 11:00").replace(tzinfo=pytz.utc),
            "image": SimpleUploadedFile(name='test.png', content=open('todos/test/test.png', 'rb').read(),
                                        content_type='image/png')
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"message": [
            ErrorDetail(string="Todo deadline isn't valid. This date has already passed.", code='invalid')]})
        delete_user(user)

    def test_post_todo_without_title(self):
        user = create_user()
        self.get_auth_token()
        data = {
            "description": "Hello",
            "deadline": datetime.datetime.fromisoformat("2022-01-01 11:00").replace(tzinfo=pytz.utc),
            "image": SimpleUploadedFile(name='test.png', content=open('todos/test/test.png', 'rb').read(),
                                        content_type='image/png')
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"message": [ErrorDetail(string='This field is required.', code='required')]})
        delete_user(user)