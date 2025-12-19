from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'


class GetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if value:
            return value
        raise serializers.ValidationError('email is required', code=400)


class OTPVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=5)


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)


class ResetPasswordSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=5)
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value
