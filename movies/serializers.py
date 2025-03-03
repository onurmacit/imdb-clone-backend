import base64
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


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class CreateCategoryCoverSerializer(serializers.Serializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    cover_base64 = serializers.CharField()

    def validate_cover_base64(self, value):
        try:
            base64.b64decode(value)
        except Exception as e:
            raise serializers.ValidationError("Invalid base64 content.")
        return value