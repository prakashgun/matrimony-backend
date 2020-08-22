from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .sample_data import Utilities
from .. import models
from .. import serializers


class PublicProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_profile_unauthenticated(self):
        res = self.client.get(Utilities.PROFILES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProfileTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = Utilities.sample_user()

        self.user2 = Utilities.sample_user(
            username='0123456789',
            password='test2',
            email='test2@example.com'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_profiles(self):
        Utilities.sample_profile(user=self.user)
        Utilities.sample_profile(user=self.user2)

        res = self.client.get(Utilities.PROFILES_URL)
        profiles = models.Profile.objects.all().order_by('-id')
        serializer = serializers.ProfileSerializer(profiles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_profile_detail(self):
        profile = Utilities.sample_profile(user=self.user)

        res = self.client.get(Utilities.profile_detail_url(profile.id))
        serializer = serializers.ProfileSerializer(profile)

        self.assertEqual(res.data, serializer.data)

    def test_create_profile(self):
        user = Utilities.sample_user(
            username='11111111',
            password='test3',
            email='test3@example.com'
        )
        res = self.client.post(Utilities.PROFILES_URL,
                               data=Utilities.profile_defaults(user=user,
                                                               api_post=True))
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
