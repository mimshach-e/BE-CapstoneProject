# Importing classes
from django_filters.rest_framework import FilterSet

from .models import Product

# Product Filter Class

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'price': ['gte', 'lte'],
            'stock_quantity': ['exact']
        }
