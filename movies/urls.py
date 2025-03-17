from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    AddCategory,
    AddCategoryCover,
    CategoryList,
    LoginView,
    MovieDetailView,
    MovieListView,
    RegisterView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("movie_list", MovieListView.as_view(), name="movie-list"),
    path("movie_detail/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("category_create", AddCategory.as_view(), name="category-create"),
    path("category_cover", AddCategoryCover.as_view(), name="category-cover"),
    path("category_list", CategoryList.as_view(), name="category-list"),
]
