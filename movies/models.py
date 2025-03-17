from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def clean(self):

        if not self.username.isalpha():
            raise ValidationError("Username must contain only letters.")

        if "@example.com" not in self.email:
            raise ValidationError("Email must be from 'example.com' domain.")

    def __str__(self):
        return self.username


class Movie(models.Model):
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    original_language = models.CharField(max_length=10, default="en")
    overview = models.TextField()
    release_date = models.DateField()
    popularity = models.FloatField(default=0)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    poster_path = models.URLField(blank=True, null=True)
    backdrop_path = models.URLField(blank=True, null=True)
    video = models.BooleanField(default=False)
    adult = models.BooleanField(default=False)

    categories = models.ManyToManyField("Category", related_name="movies")

    def __str__(self):
        return self.title

    def update_ratings(self):
        ratings = self.ratings.all()
        self.vote_count = ratings.count()
        self.vote_average = ratings.aggregate(models.Avg("score"))["score__avg"] or 0
        self.popularity = (self.vote_average * self.vote_count) / (self.vote_count + 10)
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    cover_url = CloudinaryField("category_covers", null=True, blank=True)

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, related_name="ratings")
    score = models.IntegerField(default=1)

    class Meta:
        unique_together = ("user", "movie")

    def __str__(self):
        return f"{self.user.username} → {self.movie.title} ({self.score}/10)"
