from rest_framework.test import APITestCase
from models import CustomUser, Category, Movie
from serializers import RegisterSerializer, LoginSerializer, MovieSerializer, CreateCategorySerializer, CreateCategoryCoverSerializer
import base64

class SerializerTestCase(APITestCase):

    def setUp(self):
        # Create a test user for authentication
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
            "password2": "securepassword123"
        }
        
        self.user = CustomUser.objects.create_user(
            username=self.user_data["username"], 
            email=self.user_data["email"], 
            password=self.user_data["password"]
        )
        
        # Create a category for the category tests
        self.category_data = {"name": "Test Category"}
        self.category = Category.objects.create(**self.category_data)

        # Create a movie for movie serializer tests
        self.movie_data = {
            "title": "Test Movie",
            "description": "A great movie"
        }
        self.movie = Movie.objects.create(**self.movie_data)

    def test_register_serializer_valid(self):
        serializer = RegisterSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, self.user_data["username"])
        self.assertEqual(user.email, self.user_data["email"])

    def test_register_serializer_invalid_passwords(self):
        invalid_data = self.user_data.copy()
        invalid_data["password2"] = "differentpassword"
        serializer = RegisterSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_register_serializer_invalid_email(self):
        invalid_data = self.user_data.copy()
        invalid_data["email"] = "invalidemail"
        serializer = RegisterSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_login_serializer_valid(self):
        login_data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        }
        serializer = LoginSerializer(data=login_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["user"], self.user)

    def test_login_serializer_invalid_credentials(self):
        login_data = {
            "username": self.user_data["username"],
            "password": "wrongpassword"
        }
        serializer = LoginSerializer(data=login_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["non_field_errors"][0], "Invalid username or password.")

    def test_movie_serializer(self):
        serializer = MovieSerializer(instance=self.movie)
        self.assertEqual(serializer.data["title"], self.movie_data["title"])
        self.assertEqual(serializer.data["description"], self.movie_data["description"])

    def test_create_category_serializer(self):
        category_data = {"name": "New Category"}
        serializer = CreateCategorySerializer(data=category_data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.name, category_data["name"])

    def test_create_category_cover_serializer_valid(self):
        cover_data = {
            "category_id": self.category.id,
            "cover_base64": base64.b64encode(b"dummydata").decode("utf-8")
        }
        serializer = CreateCategoryCoverSerializer(data=cover_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["category_id"], self.category.id)

    def test_create_category_cover_serializer_invalid_base64(self):
        cover_data = {
            "category_id": self.category.id,
            "cover_base64": "invalidbase64"
        }
        serializer = CreateCategoryCoverSerializer(data=cover_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("cover_base64", serializer.errors)
