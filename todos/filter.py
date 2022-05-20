from django_filters import rest_framework as filters
from .models import Todo


class TodoFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='iexact')
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')

    deadline = filters.DateTimeFilter(field_name='deadline', lookup_expr='exact')

    class Meta:
        model = Todo
        fields = ['name', 'description', 'deadline']
