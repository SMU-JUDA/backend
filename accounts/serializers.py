from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import serializers

from accounts.models import Profile

class CreateUserProfileSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Profile 
        fields = ("nickname",)

# 회원가입
class CreateUserSerializer(serializers.ModelSerializer):
    profile = CreateUserProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "profile")
        extra_kwargs = {"password": {"write_only": True}}


    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], validated_data["email"], validated_data["password"]
        )
        return user    
    
class SessionProfileSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Profile 
        fields = ("nickname",)

# 접속 유지중인지 확인
class SessionUserSerializer(serializers.ModelSerializer):
    profile = SessionProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "profile", )

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
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nickname",)

class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileUpdateSerializer(read_only=True)
    class Meta:
        model = User
        fields = ("email", "password", "profile", )


