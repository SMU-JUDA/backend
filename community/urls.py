from django.urls import path
from community.views import PostListAPI, PostDetailAPI

app_name = 'community'

urlpatterns = [
    path("post/", PostListAPI.as_view()),
    path("post/<int:pk>/", PostDetailAPI.as_view()),
]


