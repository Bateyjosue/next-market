import django_filters
from .models import * 


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = ['category', 'title']