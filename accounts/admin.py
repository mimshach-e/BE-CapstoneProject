from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Registered User model here.
admin.site.register(User, UserAdmin)
