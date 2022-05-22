from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters import rest_framework as filters

from ..serializer.todoSerializer import TodoItemsSerializer
from ....filter import TodoFilter
from ....models import Todo
from ....permissions import IsLoggedIn, IsAuthorOfTodo


class TodoItemsViewSet(ModelViewSet):
    serializer_class = TodoItemsSerializer
    parser_classes = (FormParser, MultiPartParser)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TodoFilter

    def get_queryset(self, *args, **kwargs):
        todo = Todo.objects.filter(author_id=self.request.user.id)
        return todo

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            return (IsAuthorOfTodo(),)
        else:
            return (IsLoggedIn(),)

    def get_todo_object(self, pk):
        try:
            return Todo.objects.get(id=pk)
        except Todo.DoesNotExist:
            return Response({"message": "Todo Object with given id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

    image = openapi.Parameter('image', in_=openapi.IN_FORM, description='todo image', type=openapi.TYPE_FILE, required=False)
    deadline = openapi.Parameter('deadline', in_=openapi.IN_FORM, description='todo deadline',
                                 format=openapi.FORMAT_DATE, type=openapi.TYPE_STRING, required=True)

    @swagger_auto_schema(manual_parameters=[image, deadline], request_body=TodoItemsSerializer,
                         operation_id="Post Method Todo Items", responses={status.HTTP_201_CREATED: "Success"})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'method': self.action})
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Todo created successfully"}, status=status.HTTP_201_CREATED, headers=headers)

    deadline = openapi.Parameter('deadline', in_=openapi.IN_FORM, description='todo deadline',
                                 format=openapi.FORMAT_DATE, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[image, deadline], request_body=TodoItemsSerializer,
                         operation_id="Put Method Todo Items", responses={status.HTTP_200_OK: "Success"})
    def update(self, request, *args, **kwargs):
        uuid_key = kwargs.pop('pk')
        instance = self.get_todo_object(uuid_key)
        if instance.author == request.user:
            serializer = self.get_serializer(instance, data=request.data, context={'method': self.action})
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "Todo updated successfully"}, status=status.HTTP_200_OK, headers=headers)
        else:
            return Response({"message": "Todo can't be updated. This todo doesn't belong to you."}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[image, deadline], request_body=TodoItemsSerializer,
                         operation_id="Patch Method Todo Items", responses={status.HTTP_200_OK: "Success"})
    def partial_update(self, request, *args, **kwargs):
        uuid_key = kwargs.pop('pk')
        instance = self.get_todo_object(uuid_key)
        if instance.author == request.user:
            serializer = self.get_serializer(instance, data=request.data, context={'method': self.action}, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "Todo partial updated successfully"}, status=status.HTTP_200_OK,
                            headers=headers)
        else:
            return Response({"message": "Todo can't be updated. This todo doesn't belong to you."}, status=status.HTTP_400_BAD_REQUEST)



