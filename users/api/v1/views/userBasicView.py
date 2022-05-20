from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, permission_classes

from django.conf import settings

from ....models import User
from ..serializer.userBasicSerializer import UserSerializer


class AccountProfileView(views.APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(request.user).data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
