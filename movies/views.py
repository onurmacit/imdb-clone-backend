from django.core.cache import cache
from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, CustomUser, Movie
from .serializers import (
    CreateCategoryCoverSerializer,
    CreateCategorySerializer,
    LoginSerializer,
    MovieSerializer,
    RegisterSerializer,
)
from .throttles import CustomMovieThrottle
from .utils import decode_and_upload_to_cloudinary


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            errors = serializer.errors
            priority_fields = ["email", "username", "password"]

            for field in priority_fields:
                if field in errors:
                    return Response(
                        {
                            "success": False,
                            "detail": f"{field}: {', '.join(errors[field])}",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            for field, error in errors.items():
                return Response(
                    {"success": False, "detail": f"{field}: {', '.join(error)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        with transaction.atomic():
            user = serializer.save()
            refresh_token = RefreshToken.for_user(user)

            return Response(
                {
                    "success": True,
                    "access_token": str(refresh_token.access_token),
                    "refresh_token": str(refresh_token),
                    "detail": None,
                },
                status=status.HTTP_201_CREATED,
            )


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "detail": "Invalid login information."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data["user"]
        refresh_token = RefreshToken.for_user(user)

        return Response(
            {
                "success": True,
                "access_token": str(refresh_token.access_token),
                "refresh_token": str(refresh_token),
                "detail": None,
            },
            status=status.HTTP_200_OK,
        )


class MovieListView(APIView):
    throttle_classes = [CustomMovieThrottle]

    def get(self, request):
        cache_key = "movie_list"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        cache.set(cache_key, serializer.data, timeout=60)

        return Response(serializer.data)


class MovieDetailView(APIView):
    throttle_classes = [CustomMovieThrottle]

    def get(self, request, pk):
        return Response({"message": f"Movie {pk} details"})


class AddCategory(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            category = serializer.save()
            return Response(
                {
                    "success": True,
                    "detail": "Category created successfully.",
                    "category_id": category.id,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"success": False, "detail": "Invalid data."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AddCategoryCover(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCategoryCoverSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            category_id = serializer.validated_data["category_id"]
            cover_base64 = serializer.validated_data["cover_base64"]
            try:
                category = Category.objects.get(id=category_id)
                cover_url = decode_and_upload_to_cloudinary(cover_base64)
                category.cover_url = cover_url
                category.save()
                return Response(
                    {
                        "success": True,
                        "detail": "Category cover uploaded successfully.",
                    },
                    status=status.HTTP_200_OK,
                )
            except Category.DoesNotExist:
                return Response(
                    {"success": False, "detail": "Category not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"success": False, "detail": "Invalid data."},
                status=status.HTTP_400_BAD_REQUEST,
            )
