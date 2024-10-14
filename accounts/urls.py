# Importing required and necessary functions and classes
from django.urls import path

from .views import UserLoginView, UserRegistrationView

# URL patterns for the user account management views
urlpatterns = [
    # Account Management URLs
    path('accounts/register/', UserRegistrationView.as_view(), name='register'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
]
