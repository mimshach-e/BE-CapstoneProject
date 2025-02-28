# Importing required and necessary modules, functions and classes
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import CustomUser

# A Test Class For the Account App


class AccountsTestCase(TestCase):
    def setUp(self):
        # setting up variables and user data
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@alx.com',
            'password': 'testing@123'
        }

    # A Method for testing successful user registration
    def test_user_registration(self):
        response = self.client.post(
            self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'testuser')

    # A Method for testing an unsuccessful user registration
    def test_user_registration_invalid_data(self):
        invalid_data = {
            'username': 'testuser',
            'email': 'invalid_email',
            'password': 'invalid'
        }

        response = self.client.post(
            self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testing a successul user login
    def test_user_login(self):
        # first create the user
        self.client.post(self.register_url, self.user_data, format='json')

        # now let's login
        login_data = {
            'username': 'testuser',
            'password': 'testing@123'
        }

        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        self.assertIn('username', response.data)
        self.assertIn('message', response.data)

    # Testing an unsuccessul user login
    def test_user_login_invalid_credentials(self):
        login_data = {
            'username': 'invalid-user',
            'password': 'wrongpassword'
        }

        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Testing the Token Obtain Enpoint
    def test_token_obtain(self):
        # creating user first
        self.client.post(self.register_url, self.user_data, format='json')

        # now attempt to obtain a token
        token_url = reverse('token_obtain_pair')
        token_data = {
            'username': 'testuser',
            'password': 'testing@123'
        }

        response = self.client.post(token_url, token_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    # Testing the Refresh Token Enpoint
    def test_token_refresh(self):
        # first creating a user and obtaining a token
        self.client.post(self.register_url, self.user_data, format='json')
        token_url = reverse('token_obtain_pair')
        token_data = {
            'username': 'testuser',
            'password': 'testing@123'
        }

        response = self.client.post(token_url, token_data, format='json')
        refresh_token = response.data['refresh']

        # let's try refreshing the token
        refresh_url = reverse('token_refresh')
        refresh_data = {
            'refresh': refresh_token
        }

        response = self.client.post(refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
