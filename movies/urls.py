from django.urls import path

from .views import (
    AddCategory,
    AddCategoryCover,
    AddMovie,
    CategoryList,
    GetMovies,
    LoginView,
    RateMovie,
    RegisterView,
    movie_list,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("movie_add/", AddMovie.as_view(), name="add-movie"),
    path("movie_list/", GetMovies.as_view(), name="movie-list"),
    path("category_create/", AddCategory.as_view(), name="category-create"),
    path("category_list/", CategoryList.as_view(), name="category-list"),
    path("category_cover/", AddCategoryCover.as_view(), name="category-cover"),
    path("movie_rate/", RateMovie.as_view(), name="movie-rate"),
    path("", movie_list, name="movie-list"),
]
