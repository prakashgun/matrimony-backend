from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'profile_management'

router = routers.DefaultRouter()
router.register('profiles', views.ProfileViewSet)

urlpatterns = [
    path('', include(router.urls))
]
