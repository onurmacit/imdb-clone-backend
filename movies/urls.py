from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import MovieDetailView, MovieListView, RegisterView

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/movie_list", MovieDetailView.as_view(), name="movie-list"),
    path("api/movie_detail", MovieListView.as_view(), name="movie-detail"),
]
