from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Movie
from .serializers import MovieSerializer, RegisterSerializer
from .throttles import CustomMovieThrottle


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
