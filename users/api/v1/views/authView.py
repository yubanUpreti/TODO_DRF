from django.contrib.auth.hashers import check_password
from django.conf import settings

from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError

from ....models import User
from ..serializer.authSerializer import LoginTokenSerializer, RefreshTokenSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginTokenSerializer

    def post(self, request, *args, **kwargs):
        if not User.objects.filter(email=request.data['email']).exists():
            return Response({'message': "No active account found with the given credentials"},
                            status=HTTP_401_UNAUTHORIZED)
        try:
            return super().post(request, *args, **kwargs)

        except Exception:
            return Response({'message': 'No active account found with the given credentials.'},
                            status=HTTP_401_UNAUTHORIZED)


class RefreshTokenView(TokenRefreshView):
    serializer_class = RefreshTokenSerializer


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except TokenError:
            pass
        return Response({'detail': 'Successfully logged out.'})
