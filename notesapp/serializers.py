from rest_framework import serializers
from .models import Note, User
import re
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "password",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def validate_password(self, value):
        if len(value) < 6 or len(value) > 14:
            raise serializers.ValidationError(
                "Password must be between 6 and 14 characters long."
            )

        if not re.search("[a-z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search("[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search("[0-9]", value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )

        if not re.search("[!@#$%^&*()_+=\-{}[\]:;\"'|\\,.<>?]", value):
            raise serializers.ValidationError(
                "Password must contain at least one special character."
            )

        return value

    def create(self, validated_data):
        validated_data["password"] = self.hash_password(validated_data["password"])
        return super().create(validated_data)

    def hash_password(self, password):
        return make_password(password)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        return data


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            "title",
            "content",
        ]
