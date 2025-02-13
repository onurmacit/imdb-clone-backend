from django.test import TestCase
from ..serializers import RegisterSerializer

class RegisterSerializerTests(TestCase):
    def test_valid_data(self):
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors) 

    def test_invalid_email(self):
        data = {
            'email': 'invalid.com',
            'username': 'testuser',
            'password': 'testpass123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_missing_fields(self):
        data = {'email': 'test@example.com'}
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
        self.assertIn('password', serializer.errors)
