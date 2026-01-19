from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import EmailVerificationToken

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    full_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.UUIDField()

    def validate_token(self, token):
        try:
            t = EmailVerificationToken.objects.get(token=token)
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")

        if t.used_at:
            raise serializers.ValidationError("Token already used.")
        if timezone.now() >= t.expires_at:
            raise serializers.ValidationError("Token expired.")

        return token


class LoginSerializer(TokenObtainPairSerializer):
    pass


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "full_name", "is_verified")
        read_only_fields = ("email", "is_verified")
