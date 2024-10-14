# Importing modules and classes
from django.contrib import admin

from .models import Category, Discount, Product

# Register Products in Admin

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'stock_quantity',
                    'created_at', 'created_by']
    list_filter = ['created_at']

# Registering Categories in Admin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'created_by']
    list_filter = ['name']

# Registering Discounts in Admin

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_type', 'value', 'start_date', 'end_date', 'active',]
    list_filter = ['name', 'active']
