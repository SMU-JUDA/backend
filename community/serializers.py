from dataclasses import field
from email.mime import image
from community.models import Post
from rest_framework import serializers

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
                'id',
                'title',
                'writer_nickname', 
                'create_dt',
        ]
    
    writer_nickname = serializers.SerializerMethodField("get_writer_nickname")

    def get_writer_nickname(self, obj):
        return obj.writer.profile.nickname

class PostListSuccessSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="글 번호")
    title = serializers.CharField(help_text="글 제목")
    writer_nickname = serializers.CharField(help_text="작성자 닉네임")
    create_dt = serializers.DateTimeField(help_text="글 작성시간")

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
                'title',
                'content', 
        ]

class PostCreateUpdateParamsSerializer(serializers.Serializer):
    title = serializers.CharField(help_text='글 제목')
    content = serializers.CharField(help_text='내용')


class PostDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text='글 번호')
    title = serializers.CharField(help_text='글 제목')
    writer_nickname = serializers.SerializerMethodField("get_writer_nickname")
    content = serializers.CharField(help_text='글 내용')
    create_dt = serializers.DateTimeField(help_text="글 작성 시간")
    update_dt = serializers.DateTimeField(help_text="글 수정 시간")

    def get_writer_nickname(self, obj):
        return obj.writer.profile.nickname


class PostDetailSuccessSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="글 번호")
    title = serializers.CharField(help_text="글 제목")
    writer_nickname = serializers.CharField(help_text="작성자 닉네임")
    content = serializers.CharField(help_text="글 내용")
    create_dt = serializers.DateTimeField(help_text="글 작성 시간")
    update_dt = serializers.DateTimeField(help_text="글 수정 시간")