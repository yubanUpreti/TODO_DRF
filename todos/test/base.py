import datetime

import pytz
from users.models import User
from ..models import Todo
from rest_framework.test import force_authenticate, APIRequestFactory, APIClient


def create_user(email="client@test.com", password="Admin@123"):
    user = User.objects.create_user(email, password)
    return user


def delete_user(user):
    user.delete()


def create_todo(name="Test Todo", description="", deadline="2022-06-01 11:00"):
    user = create_user()
    todo = Todo.objects.create(name=name, description=description, deadline=datetime.datetime.fromisoformat(deadline).replace(tzinfo=pytz.utc), author=user)
    return user, todo
