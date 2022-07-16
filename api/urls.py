from django.urls import include, path
from api.views import RegistrationAPI, LoginAPI

app_name = 'api'

urlpatterns = [
    path(r"register/", RegistrationAPI.as_view()),
    path(r"login/", LoginAPI.as_view()),
    path(r"auth/", include("knox.urls")),
]

