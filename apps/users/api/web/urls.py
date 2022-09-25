from django.urls import path

from apps.users.api.web.views.views import APILoginUser, APIUserInfo

urlpatterns = [
    path("v1/login/", APILoginUser.as_view()),
    path("v1/UseInf/", APIUserInfo.as_view()),
]
