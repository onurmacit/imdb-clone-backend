from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import AddCategory, MovieDetailView, MovieListView, RegisterView, AddCategoryCover

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/movie_list", MovieDetailView.as_view(), name="movie-list"),
    path("api/movie_detail", MovieListView.as_view(), name="movie-detail"),
    path("api/category_create", AddCategory.as_view(), name="category-create"),
    path("api/category_cover", AddCategoryCover.as_view(), name="category-cover"),
]
