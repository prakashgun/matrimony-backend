from rest_framework.serializers import ModelSerializer

from .models import Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        read_only_fields = ('id',)
        fields = '__all__'
