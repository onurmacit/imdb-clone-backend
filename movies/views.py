from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, CustomUser, Movie, Rating
from .serializers import (
    CategorySerializer,
    CreateCategoryCoverSerializer,
    CreateCategorySerializer,
    LoginSerializer,
    MovieCreateSerializer,
    MovieListSerializer,
    RatingSerializer,
    RegisterSerializer,
)
from .utils import decode_and_upload_to_cloudinary


def movie_list(request):
    movies = Movie.objects.all().order_by("-popularity")
    paginator = Paginator(movies, 8)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "movies.html", {"movies": page_obj})


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


class AddMovie(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MovieCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "detail": "Movie added successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetMovies(APIView):
    def get(self, request, *args, **kwargs):
        movies = Movie.objects.all().order_by("-popularity")

        page_number = request.query_params.get("page", 1)
        paginator = Paginator(movies, per_page=10)
        page_obj = paginator.get_page(page_number)

        serializer = MovieListSerializer(
            page_obj, many=True, context={"request": request}
        )

        response_data = {"page": page_obj.number, "results": serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)


class CategoryList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()

        serializer = CategorySerializer(categories, many=True)

        return Response(
            {
                "success": True,
                "detail": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


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

                file_name = f"category_{category.id}_{category.category_name}"

                cover_url = decode_and_upload_to_cloudinary(
                    base64_str=cover_base64,
                    folder_name="category_covers",
                    file_name=file_name,
                )

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
            except ValueError as e:
                return Response(
                    {"success": False, "detail": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"success": False, "detail": "Invalid data."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RateMovie(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        movie_id = request.data.get("movie")
        score = request.data.get("score")

        if not movie_id or not score:
            return Response(
                {"success": False, "detail": "Movie ID and score are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        movie_id = get_object_or_404(Movie, id=movie_id)
        serializer = RatingSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "detail": "Rating submitted successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, *args, **kwargs):
        movie_id = request.data.get("movie")

        if not movie_id:
            return Response(
                {"success": False, "detail": "Movie ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        movie = get_object_or_404(Movie, id=movie_id)
        rating = Rating.objects.filter(user=request.user, movie=movie).first()

        if rating:
            rating.delete()
            movie.update_ratings()
            return Response(
                {"success": True, "detail": "Rating removed successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"success": False, "detail": "Rating not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
