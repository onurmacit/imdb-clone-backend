from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import CustomUser


class RegisterViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("register")
        self.valid_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123",
        }
        self.invalid_email_data = {
            "email": "test@invalid.com",
            "username": "testuser",
            "password": "testpassword123",
        }
        self.invalid_username_data = {
            "email": "test@example.com",
            "username": "testuser123",
            "password": "testpassword123",
        }

    def test_register_success(self):
        response = self.client.post(self.url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_register_failure_invalid_email(self):
        response = self.client.post(self.url, self.invalid_email_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email must be from", response.data["email"][0])

    def test_register_failure_invalid_username(self):
        response = self.client.post(self.url, self.invalid_username_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Username must contain only letters", response.data["username"][0]
        )

    def test_register_failure_missing_fields(self):
        response = self.client.post(
            self.url, {"email": "test@example.com"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertSetEqual(set(response.data.keys()), {"username", "password"})

    def tearDown(self):
        CustomUser.objects.all().delete()
