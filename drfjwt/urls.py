"""
URL configuration for drfjwt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.urls import include, path
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from tasks.models import Task


### USERS router
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            "url",
            "username",
            "email",
            "is_staff",
            "is_active",
            "is_superuser",
            "password",
            "first_name",
            "last_name",
        ]


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
user_router = routers.DefaultRouter()
user_router.register(r"users", UserViewSet)


### TASKS router
# Serializers define the API representation.
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "isFav",
        ]


# ViewSets define the view behavior.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# Routers provide an easy way of automatically determining the URL conf.
taskRouter = routers.DefaultRouter()
taskRouter.register(r"task", TaskViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/obtain/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),  # login/ and logout/ routes for browsable API
    path("api-users/", include(user_router.urls)),
    path("tasks_test_api/", include(taskRouter.urls)),
    path("news_api/", include("newsapi.urls")),
]
