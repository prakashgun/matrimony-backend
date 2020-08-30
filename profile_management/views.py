from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . import models, serializers, permissions, filters


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializer
    queryset = models.Profile.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.ProfileFilter

    def get_queryset(self):
        return self.queryset.order_by('-id')


class InterestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InterestSerializer
    permission_classes = (
        IsAuthenticated,
        permissions.InterestDecisionAndDelete,
    )
    queryset = models.Interest.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        return self.queryset.filter(
            Q(from_profile__user=self.request.user) |
            Q(to_profile__user=self.request.user)
        ).order_by('-id')

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = serializers.InterestAcceptSerializer

        return serializer_class


class ShortlistViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ShortlistSerializer
    queryset = models.Shortlist.objects.all()
    permission_classes = (
        IsAuthenticated,
    )

    def get_queryset(self):
        return self.queryset.filter(from_profile__user=self.request.user) \
            .order_by('-id')
