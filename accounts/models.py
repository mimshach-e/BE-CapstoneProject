from django.db import models
from django.contrib.auth.models import AbstractUser

# User Model
class User(AbstractUser): 
    email = models.EmailField(unique=True)
    
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        unique_together = ['username', 'email']

        def __str__(self):
            return self.username

