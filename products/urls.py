from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CreateCategoryView, ListCategoryView, UpdateCategoryView, DetailCategoryView,
    DeleteCategoryView, CreateProductView, ListProductView, DetailProductView, 
    UpdateProductView, DeleteProductView, RatingView, WishListView, DiscountView
) 

router = DefaultRouter()
router.register(r'products/(?P<product_id>\d+)/ratings', RatingView, basename='product-ratings')
router.register(r'products/(?P<product_id>\d+)/wishlist', WishListView, basename='product-wishlist')
router.register(r'products/(?P<product_id>\d+)/discounts', DiscountView, basename='product-discount')

urlpatterns = [
    # Category Enpoint URLs
    path('category/create/', CreateCategoryView.as_view(), name='category_create'),
    path('category/', ListCategoryView.as_view(), name='category_list'),
    path('category/<int:pk>/', DetailCategoryView.as_view(), name='category_detail'),
    path('category/update/<int:pk>/', UpdateCategoryView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', DeleteCategoryView.as_view(), name='category_delete'),

    # Products Endpoint URLs
    path('products/create/', CreateProductView.as_view(), name='products-create'),
    path('products/', ListProductView.as_view(), name='products-list'),
    path('products/<int:pk>/', DetailProductView.as_view(), name='products-detail'),
    path('products/update/<int:pk>/', UpdateProductView.as_view(), name='products-update'),
    path('products/delete/<int:pk>/', DeleteProductView.as_view(), name='products-delete'),

    # Viewset Endpoint URL for Ratings, Wishlist & Discounts
    path('', include(router.urls)),

]  