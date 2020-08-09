from rest_framework import viewsets

from . import models
from . import serializers


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializer
    queryset = models.Profile.objects.all()

    def get_queryset(self):
        return self.queryset.order_by('-id')
