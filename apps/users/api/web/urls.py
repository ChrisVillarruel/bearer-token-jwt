from django.urls import path

from apps.users.api.web.views.views import APILoginUser, APIUserInfo, APIUpdatePasswordUser

urlpatterns = [
    path("v1/login/", APILoginUser.as_view()),
    path("v1/UseInf/", APIUserInfo.as_view()),
    path("v1/UpdPassUsr/", APIUpdatePasswordUser.as_view()),
]
