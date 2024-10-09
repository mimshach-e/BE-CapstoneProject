from django.contrib import admin
from .models import Product, Category

# Registered Prodel Model.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'stock_quantity', 
                    'created_at', 'created_by']
    list_filter = ['created_at']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'created_by']
    list_filter = ['name']
