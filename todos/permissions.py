from rest_framework import permissions, status
from rest_framework.response import Response

from .models import Todo


class IsLoggedIn(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAuthorOfTodo(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, todo):
        if request.user:
            return todo.author == request.user
        return False
