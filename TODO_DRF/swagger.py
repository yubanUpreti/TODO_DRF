from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


swagger_info = openapi.Info(
   title="TODO DRF APIs",
   default_version='v1',
   description="Simple Coding Challenge TODO API",
   contact=openapi.Contact(email="yubanupreti@gmail.com"),
   license=openapi.License(name="BSD License"),
)

drf_yasg_swagger_view = get_schema_view(
   swagger_info,
   public=False,
   permission_classes=[permissions.AllowAny],
)
