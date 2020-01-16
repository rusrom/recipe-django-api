from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@check.io',
            'password': 'f2f234f23',
            'name': 'John Dou'
        }

        res = self.client.post(CREATE_USER_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_already_exists(self):
        """Test creating user that already exists fails"""
        payload = {'email': 'test@check.io', 'password': 'f2f234f23'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_to_short(self):
        """Test that password must be greater than 5 characters long"""
        payload = {'email': 'test@check.io', 'password': 'pw'}

        res = self.client.post(CREATE_USER_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token created for user"""
        payload = {'email': 'test@check.io', 'password': 'f2f234f23'}
        create_user(**payload)

        res = self.client.post(TOKEN_URL, data=payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@check.io', password='f2f234f23')
        payload = {'email': 'test@check.io', 'password': 'wrong_password'}
        res = self.client.post(TOKEN_URL, data=payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@check.io', 'password': 'wrong_password'}
        res = self.client.post(TOKEN_URL, data=payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {'email': 'test@check.io', 'password': ''}
        res = self.client.post(TOKEN_URL, data=payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
