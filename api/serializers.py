import base64
from dataclasses import field
import email
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from api.models import Profile

# 회원가입
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], validated_data["email"], validated_data["password"]
        )
        return user

class ReturnUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    nickname = serializers.CharField()
    email = serializers.EmailField()

class SuccesssUserSerializer(serializers.Serializer):
    user = ReturnUserSerializer()
    token = serializers.CharField()

# 접속 유지중인지 확인
class SessionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", )

# 로그인
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")

# 프로필 업데이트
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nickname", "image", )

class ProfileParamsSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    image = serializers.ImageField()

class ProfileSuccessSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    image = serializers.ImageField()

class ProfileViewSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    image = serializers.ImageField()
