from django.urls import reverse
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

    def test_get_todo_valid_user(self):
        user, todo = create_todo()
        self.get_auth_token()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['author']['email'], 'client@test.com')
        self.url_e = reverse_lazy('todos:todo-urls-detail', kwargs={'pk': todo.id})
        self.client.delete(self.url_e, format='json')
        delete_user(user)

    def test_get_todo_invalid_user(self):
        user, todo = create_todo()
        user1 = create_user("user@not.com", "Admin!123@")
        self.get_auth_token("user@not.com", "Admin!123@")
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], [])
        delete_user(user)
        delete_user(user1)

    def test_get_todo_valid_pk(self):
        user, todo = create_todo()
        self.get_auth_token()
        self.url_e = reverse_lazy('todos:todo-urls-detail', kwargs={'pk': todo.id})
        response = self.client.get(self.url_e, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Todo')
        delete_user(user)

    def test_get_todo_invalid_pk(self):
        user, todo = create_todo()
        self.get_auth_token()
        self.url_e = reverse_lazy('todos:todo-urls-detail', kwargs={'pk': 'abc'})
        response = self.client.get(self.url_e, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'detail': 'Not found.'})
        delete_user(user)


