import datetime

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

    def get_auth_token(self, email="client@test.com", password="Admin@123"):
        data = {
            "email": email,
            "password": password
        }
        tkn = self.client.post(self.signin_url, data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tkn.data['access'])

    def test_put_todo_valid_pk(self):
        user, todo = create_todo()
        self.get_auth_token()
        self.url_e = reverse_lazy('todos:todo-urls-detail', kwargs={'pk': todo.id})
        data = {
            "name": "Test Todo Updated",
            "description": "Hello",
            "deadline": datetime.datetime.fromisoformat("2022-07-01 11:00").replace(tzinfo=pytz.utc),
            "image": SimpleUploadedFile(name='test.png', content=open('todos/test/test.png', 'rb').read(),
                                        content_type='image/png')
        }
        response = self.client.put(self.url_e, data, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Todo updated successfully"})
        delete_user(user)

    def test_put_others_todo_valid_pk(self):
        user, todo = create_todo()
        user1 = create_user("user@not.com", "Admin!123@")
        self.get_auth_token("user@not.com", "Admin!123@")
        self.url_e = reverse_lazy('todos:todo-urls-detail', kwargs={'pk': todo.id})
        data = {
            "name": "Test Todo Updated",
            "description": "Hello",
            "deadline": datetime.datetime.fromisoformat("2022-07-01 11:00").replace(tzinfo=pytz.utc),
            "image": SimpleUploadedFile(name='test.png', content=open('todos/test/test.png', 'rb').read(),
                                        content_type='image/png')
        }
        response = self.client.put(self.url_e, data, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'message': "Todo can't be updated. This todo doesn't belong to you."})
        delete_user(user)
        delete_user(user1)

