from django.test import TestCase
from django.contrib.auth import get_user_model


email = 'balisong@knives.io'
password = 'Te$tpaaS$123'


class ModelTests(TestCase):
    def test_create_user_with_emai_successful(self):
        """Test creating new user with an email is successful"""
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for new user is normalized"""
        email = 'balisong@KNIVES.IO'
        user = get_user_model().objects.create_user(email, password)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email rises error"""
        email = None
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email, password)

    def test_create_new_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(email, password)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_stuff)
