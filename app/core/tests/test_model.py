from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_emai_successful(self):
        """Test creating new user with an email is successful"""
        email = 'balisong@knives.io'
        password = 'Te$tpaaS$123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
