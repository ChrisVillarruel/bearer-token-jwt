from django.urls import path
from rest_framework.routers import SimpleRouter
from apps.users.api.web.views.views import (
    APILoginUser,
    APIUserInfo,
    APIUpdatePasswordUser,
    APIForgotPassword
)

routers = SimpleRouter()
routers.register("v1/new-pass", APIForgotPassword, basename="forgot-password")

urlpatterns = [
    path("v1/edit-password/", APIUpdatePasswordUser.as_view()),
    path("v1/sig-in/", APILoginUser.as_view()),
    path("v1/", APIUserInfo.as_view()),
]

urlpatterns += routers.urls
