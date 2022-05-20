from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views.authView import LoginView, LogoutView, RefreshTokenView
from .views.signupView import RegisterView


urlpatterns = [
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/logout', LogoutView.as_view(), name="logout"),
    path('auth/token/refresh', RefreshTokenView.as_view(), name="refresh-token"),
    path('auth/register', RegisterView.as_view(), name="signup"),
]
