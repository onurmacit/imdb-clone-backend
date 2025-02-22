from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ..views import RegisterView


class UrlsTests(TestCase):
    def test_register_url(self):
        url = reverse("register")
        self.assertEqual(url, "/api/register/")
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_token_obtain_url(self):
        url = reverse("token_obtain_pair")
        self.assertEqual(url, "/api/token/")
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)

    def test_token_refresh_url(self):
        url = reverse("token_refresh")
        self.assertEqual(url, "/api/token/refresh/")
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)
