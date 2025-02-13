from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import CustomUser

class CustomUserModelTests(TestCase):
    def setUp(self):
        self.valid_user = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword123'
        }

    def test_create_user_success(self):
        user = CustomUser.objects.create_user(**self.valid_user)
        self.assertEqual(user.email, self.valid_user['email'])
        self.assertEqual(user.username, self.valid_user['username'])
        self.assertTrue(user.check_password(self.valid_user['password']))

    def test_create_user_invalid_username(self):
        user = CustomUser(email='test@example.com', username='invalid_user123')
        with self.assertRaisesMessage(ValidationError, 'Username must contain only letters.'):
            user.full_clean()

    def test_create_user_invalid_email(self):
        user = CustomUser(email='invalid.com', username='testuser')
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', username='testuser', password='testpassword123')

    def test_str_method(self):
        user = CustomUser.objects.create_user(**self.valid_user)
        self.assertEqual(str(user), self.valid_user['username'])
