from rest_framework.serializers import ModelSerializer

from . import models


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = models.Profile
        read_only_fields = ('id',)
        fields = '__all__'


class InterestSerializer(ModelSerializer):
    class Meta:
        model = models.Interest
        read_only_fields = ('id',)
        fields = '__all__'


class ShortlistSerializer(ModelSerializer):
    class Meta:
        model = models.Shortlist
        read_only_fields = ('id',)
        fields = '__all__'
