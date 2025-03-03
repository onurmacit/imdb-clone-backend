from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Movie
from .serializers import (
    CreateCategoryCoverSerializer,
    CreateCategorySerializer,
    MovieSerializer,
    RegisterSerializer,
)
from .throttles import CustomMovieThrottle
from .utils import decode_and_upload_to_cloudinary


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
