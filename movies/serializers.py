import base64

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Category, CustomUser, Movie


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


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class CreateCategoryCoverSerializer(serializers.Serializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    cover_base64 = serializers.CharField()

    def validate_cover_base64(self, value):
        try:
            if len(value) % 4 != 0:
                raise serializers.ValidationError("Base64 string has invalid length.")
            base64.b64decode(value)
        except Exception:
            raise serializers.ValidationError("Invalid base64 content.")
        return value
