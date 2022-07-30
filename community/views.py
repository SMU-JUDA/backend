
from community.models import Post
from community.serializers import PostCreateUpdateSerializer, PostListSerializer, PostListSuccessSerializer, PostDetailSerializer, PostCreateUpdateParamsSerializer, PostDetailSuccessSerializer

from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from knox.auth import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema

class PostListAPI(APIView):
    authentication_classes = [TokenAuthentication]
    parser_classes = (MultiPartParser, ) 

    @swagger_auto_schema(operation_description='글 목록', request_body=None, responses={"200": PostListSuccessSerializer(many=True)}) 
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description='글 생성', request_body=PostCreateUpdateParamsSerializer, responses={"200": PostCreateUpdateParamsSerializer}) 
    def post(self, request, format=None):
        serializer = PostCreateUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(writer=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, ) 

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description='글 조회', request_body=None, responses={"200": PostDetailSuccessSerializer}) 
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description='글 수정', request_body=PostCreateUpdateParamsSerializer, responses={"200": PostCreateUpdateParamsSerializer}) 
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostCreateUpdateSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description='글 삭제', ) 
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)