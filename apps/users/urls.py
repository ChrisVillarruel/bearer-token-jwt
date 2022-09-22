from django.urls import path, include

urlpatterns = [
    path('web/', include("apps.users.api.web.urls")),
]
