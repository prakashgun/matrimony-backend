from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import generics, permissions

from .serializers import UserSerializer, GroupSerializer
from .permissions import IsPostOrIsAuthenticated


class UserList(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = [IsPostOrIsAuthenticated]

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
