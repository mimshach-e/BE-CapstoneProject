# Importing required and necessary modules, functions and classes
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import CustomUser


# CustomUser Serializer: serializes the CustomUser model
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # hides password

    # Ensuring password is hashed for security reasons
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    # Validating the users data
    def validate(self, data):
        user = authenticate(
            username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid username or password')
        return data
