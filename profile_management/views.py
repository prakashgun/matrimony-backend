from rest_framework import viewsets, mixins

from . import models
from . import serializers


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializer
    queryset = models.Profile.objects.all()

    def get_queryset(self):
        return self.queryset.order_by('-id')


class InterestViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = models.Interest.objects.all()
