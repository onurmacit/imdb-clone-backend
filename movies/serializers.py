import base64
import logging

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Category, CustomUser, Movie, Rating
from .utils import decode_and_upload_to_cloudinary


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {
            "email": {
                "required": True,
                "validators": [
                    UniqueValidator(
                        queryset=CustomUser.objects.all(),
                        message="This email address is already in use.",
                    )
                ],
            }
        }

    def validate(self, data):
        if data["password"] != data.pop("password2"):
            raise serializers.ValidationError({"password": "Passwords do not match."})

        validate_password(data["password"])
        return data

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        data["user"] = user
        return data


class MovieCreateSerializer(serializers.ModelSerializer):
    poster_base64 = serializers.CharField(write_only=True, required=False)
    backdrop_base64 = serializers.CharField(write_only=True, required=False)
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), required=False
    )

    class Meta:
        model = Movie
        fields = [
            "title",
            "original_title",
            "original_language",
            "overview",
            "release_date",
            "poster_path",
            "backdrop_path",
            "video",
            "adult",
            "categories",
            "poster_base64",
            "backdrop_base64",
        ]

    def create(self, validated_data):
        categories_data = validated_data.pop("categories", [])
        poster_base64 = validated_data.pop("poster_base64", None)
        backdrop_base64 = validated_data.pop("backdrop_base64", None)

        movie = Movie.objects.create(**validated_data)

        if categories_data:
            movie.categories.set(categories_data)

        try:
            if poster_base64:
                movie.poster_path = decode_and_upload_to_cloudinary(
                    base64_str=poster_base64,
                    folder_name="movies/posters",
                    file_name=f"movie_{movie.id}_poster",
                )
            if backdrop_base64:
                movie.backdrop_path = decode_and_upload_to_cloudinary(
                    base64_str=backdrop_base64,
                    folder_name="movies/backdrops",
                    file_name=f"movie_{movie.id}_backdrop",
                )
            movie.save()
        except ValueError as e:
            movie.delete()
            raise serializers.ValidationError(str(e))

        return movie


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "category_name"]


class MovieListSerializer(serializers.ModelSerializer):
    genre_ids = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            "adult",
            "backdrop_path",
            "genre_ids",
            "id",
            "original_language",
            "original_title",
            "overview",
            "popularity",
            "poster_path",
            "release_date",
            "title",
            "video",
            "vote_average",
            "vote_count",
            "rating",
        ]

    def get_genre_ids(self, obj):
        return list(obj.categories.values_list("id", flat=True))

    def get_rating(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            rating = obj.ratings.filter(user=request.user).first()
            return rating.score if rating else 0
        return 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["vote_average"] = round(representation["vote_average"], 2)
        return representation


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_name"]


logger = logging.getLogger(__name__)


class CreateCategoryCoverSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    cover_base64 = serializers.CharField()

    def validate_cover_base64(self, value):
        try:
            if value.startswith("data:image"):
                value = value.split("base64,")[1]

            if len(value) % 4 != 0:
                value += "=" * (4 - len(value) % 4)

            base64.b64decode(value)
        except Exception as e:
            logger.error(f"Base64 validation error: {e}")
            raise serializers.ValidationError("Invalid base64 content.")
        return value


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["movie", "score"]

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Rating must be between 1 and 10.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        movie = validated_data["movie"]
        score = validated_data["score"]

        score = round(score, 2)

        rating, created = Rating.objects.update_or_create(
            user=user, movie=movie, defaults={"score": score}
        )

        movie.update_ratings()
        return rating
