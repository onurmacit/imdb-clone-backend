from django.urls import reverse
from models import Category, CustomUser, Movie
from rest_framework import status
from rest_framework.test import APITestCase


class APITestCaseExample(APITestCase):

    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
            "password2": "securepassword123",
        }

        self.user = CustomUser.objects.create_user(
            username=self.user_data["username"],
            email=self.user_data["email"],
            password=self.user_data["password"],
        )

        self.category_data = {"name": "Test Category"}
        self.category = Category.objects.create(**self.category_data)
        self.movie = Movie.objects.create(
            title="Test Movie", description="A great movie"
        )

        # URLs
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.movie_list_url = reverse("movie-list")
        self.movie_detail_url = reverse("movie-detail")
        self.category_create_url = reverse("category-create")
        self.category_cover_url = reverse("category-cover")

    def test_register_view(self):
        # Test successful registration
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

        # Test invalid registration (passwords do not match)
        invalid_data = self.user_data.copy()
        invalid_data["password2"] = "differentpassword"
        response = self.client.post(self.register_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "password: Passwords do not match.")

    def test_login_view(self):
        # Test successful login
        login_data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

        # Test invalid login (incorrect password)
        invalid_login_data = {
            "username": self.user_data["username"],
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, invalid_login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid login information.")

    def test_movie_list_view(self):
        # Test movie list
        response = self.client.get(self.movie_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_movie_detail_view(self):
        # Test movie detail (dummy test since logic not implemented)
        response = self.client.get(self.movie_detail_url, {"pk": self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], f"Movie {self.movie.id} details")

    def test_add_category_view(self):
        # Test add category (authenticated user)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.category_create_url, self.category_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["detail"], "Category created successfully.")
        self.assertEqual(response.data["category_id"], self.category.id)

        # Test add category without authentication
        self.client.logout()
        response = self.client.post(
            self.category_create_url, self.category_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_category_cover_view(self):
        # Test add category cover (authenticated user)
        cover_data = {
            "category_id": self.category.id,
            "cover_base64": "fake_base64_data",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.category_cover_url, cover_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["detail"], "Category cover uploaded successfully."
        )

        # Test category not found
        invalid_cover_data = cover_data.copy()
        invalid_cover_data["category_id"] = 9999  # Non-existent category
        response = self.client.post(
            self.category_cover_url, invalid_cover_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Category not found.")

    def test_cache_movie_list_view(self):
        # Test caching in movie list view
        response = self.client.get(self.movie_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Now retrieve again to check if cached response is returned
        response_cached = self.client.get(self.movie_list_url)
        self.assertEqual(response_cached.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_cached.data)
