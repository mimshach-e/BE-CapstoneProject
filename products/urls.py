# Importing modules, functions and classes
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CreateCategoryView, CreateProductView, DeleteCategoryView,
                    DeleteProductView, DetailCategoryView, DetailProductView,
                    DiscountView, ListCategoryView, ListProductView,
                    RatingView, UpdateCategoryView, UpdateProductView,
                    WishListView)

router = DefaultRouter()

# Viewset Routers for Product Rating, Wishlist and Discount
router.register(r'products/(?P<product_id>\d+)/ratings',
                RatingView, basename='product-ratings')
router.register(r'products/(?P<product_id>\d+)/wishlist',
                WishListView, basename='product-wishlist')
router.register(r'products/(?P<product_id>\d+)/discounts',
                DiscountView, basename='product-discount')

urlpatterns = [
    # Category Enpoint URLs
    path('category/create/', CreateCategoryView.as_view(), name='category_create'),
    path('category/', ListCategoryView.as_view(), name='category_list'),
    path('category/<int:pk>/', DetailCategoryView.as_view(), name='category_detail'),
    path('category/<int:pk>/update/',
         UpdateCategoryView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/',
         DeleteCategoryView.as_view(), name='category_delete'),

    # Products Endpoint URLs
    path('products/create/', CreateProductView.as_view(), name='products-create'),
    path('products/', ListProductView.as_view(), name='products-list'),
    path('products/<int:pk>/', DetailProductView.as_view(), name='products-detail'),
    path('products/<int:pk>/update/',
         UpdateProductView.as_view(), name='products-update'),
    path('products/<int:pk>/delete/',
         DeleteProductView.as_view(), name='products-delete'),

    # Viewset Endpoint URL for Ratings, Wishlist & Discounts
    path('', include(router.urls)),

]
