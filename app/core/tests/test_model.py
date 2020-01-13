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

    def test_new_user_email_normalized(self):
        """Test the email for new user is normalized"""
        email = 'balisong@KNIVES.IO'
        password = 'Te$tpaaS$123'
        user = get_user_model().objects.create_user(email, password)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email rises error"""
        email = None
        password = 'Te$tpaaS$123'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email, password)
