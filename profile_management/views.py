from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from . import models, serializers, permissions


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
    serializer_class = serializers.InterestSerializer
    permission_classes = (
        IsAuthenticated,
        permissions.IsInterestReceiverOrReadOnly,
        permissions.IsOwnInterestOrDisallow
    )
    queryset = models.Interest.objects.all()


class ShortlistViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ShortlistSerializer
    queryset = models.Shortlist.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.IsOwnShortlistOrDisallow
    )

    def get_queryset(self):
        return self.queryset.filter(from_profile__user=self.request.user) \
            .order_by('-id')
