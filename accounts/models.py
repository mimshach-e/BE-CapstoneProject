# Importing required and necessary modules and classes
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        Permission, PermissionsMixin)
from django.db import models
from django.utils.translation import gettext_lazy as _

# Defined a CustomUserManager class which subclassed the BaseUserManager class


class CustomUserManager(BaseUserManager):
    # For creating normal users
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError(_('The Username field must be set'))
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # For creating superusers
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)

# Defined a CutomUser model which is an object of the CustomUserManager class


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=125, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
