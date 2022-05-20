"""TODO_DRF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/v1/', include('todos.api.v1.urls')),
    path('api/v1/', include('users.api.v1.urls')),
]

if settings.DEBUG:
    # serve media
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    from django.views.generic import RedirectView
    from .swagger import drf_yasg_swagger_view

    urlpatterns += [
        path('', RedirectView.as_view(url='api/swagger/', permanent=True)),
        path('api/swagger/', drf_yasg_swagger_view.with_ui('swagger', cache_timeout=0), name='drf_yasg_swagger_view'),

    ]
