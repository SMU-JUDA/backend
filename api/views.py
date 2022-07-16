from rest_framework import generics, status
from rest_framework.response import Response

from knox.models import AuthToken
from api.serializers import CreateUserSerializer, SuccesssUserSerializer, SessionUserSerializer, LoginUserSerializer
from drf_yasg.utils import swagger_auto_schema
from api.api_params import register_params, login_params

import re 

def email_verification(email):
    p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return p.match(email)

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    @swagger_auto_schema(tags=['회원가입'], request_body=register_params, responses={"200": SuccesssUserSerializer}) 
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

    @swagger_auto_schema(tags=['로그인'], request_body=login_params, responses={"200": SuccesssUserSerializer})
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