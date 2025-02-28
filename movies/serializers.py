import cloudinary
from rest_framework import serializers

from .models import Category, CustomUser, Movie


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if "@example.com" not in value:
            raise serializers.ValidationError(
                "Email must be from 'example.com' domain."
            )
        return value

    def validate_username(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Username must contain only letters.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "cover_image", "cover_image_url"]

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            return cloudinary.utils.cloudinary_url(
                obj.cover_image.public_id, format="jpg", quality="auto", secure=True
            )[0]
        return None
