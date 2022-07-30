from django.urls import include, path
from api.views import ProfileUpdateAPI, RegistrationAPI, UserSessionAPI, LoginAPI

app_name = 'api'

urlpatterns = [
    path(r"auth/register/", RegistrationAPI.as_view()),
    path(r"auth/login/", LoginAPI.as_view()),
    path(r"auth/user/", UserSessionAPI.as_view()),
    path(r"auth/profile/update/", ProfileUpdateAPI.as_view()),

    path(r"auth/", include("knox.urls")),
]


