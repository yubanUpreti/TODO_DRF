import uuid

from django.db import models
from django.utils import timezone

from users.models import User


class Todo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=100, blank=True)
    image = models.ImageField(upload_to='static/images/todo/', blank=True)
    deadline = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo_author")

    def __str__(self):
        return self.name
