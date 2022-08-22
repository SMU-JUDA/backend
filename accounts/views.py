from django.http import Http404
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from knox.models import AuthToken
from accounts.models import Profile
from accounts.serializers import CreateUserSerializer, SessionUserSerializer, SuccesssUserSerializer,SessionUserSerializer, LoginUserSerializer, UserUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from accounts.api_params import register_params, login_params

import re 

def email_verification(email):
    p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return p.match(email)

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    @swagger_auto_schema(operation_description='회원가입', request_body=register_params, responses={"200": SuccesssUserSerializer}) 
    def post(self, request, *args, **kwargs):
        if len(request.data["username"]) < 6:
            body = {"message": "아이디의 길이가 짧습니다. 6자리 이상의 아이디를 입력해주세요."}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        email = request.data["email"]
        
        if not email_verification(email):
            return Response("검증되지 않은 이메일입니다. 다시 확인헤주세요.", status=status.HTTP_400_BAD_REQUEST)

        if len(request.data["password"]) < 4:
            body = {"message": "비밀번호의 길이가 짧습니다. 4자리 이상의 아이디를 입력해주세요."}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user": SessionUserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    @swagger_auto_schema(operation_description='로그인', request_body=login_params, responses={"200": SuccesssUserSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": SessionUserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )

class UserSessionAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SessionUserSerializer
 
    @swagger_auto_schema(operation_description='유저 세션 확인', request_body=None, responses={"200": SessionUserSerializer})
    def get(self, request, format=None):
        user = self.request.user
        serializer = SessionUserSerializer(user)
        return Response(serializer.data)

class ProfileUpdateAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, JSONParser, ) 

    def get_object(self, pk):
        try: 
            return Profile.objects.get(user_pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description='프로필 등록 및 수정', request_body= UserUpdateSerializer, responses={"200": UserUpdateSerializer}) 
    def put(self, request):
        profile = self.get_object(self.request.user.id)
        
        serializer = UserUpdateSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

