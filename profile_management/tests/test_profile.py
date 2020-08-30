import datetime

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

        self.user3 = Utilities.sample_user(
            username='1234512345',
            password='test3',
            email='test3@example.com'
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
            password='test_create_profile',
            email='test_create_profile@example.com'
        )
        res = self.client.post(Utilities.PROFILES_URL,
                               data=Utilities.profile_defaults(user=user,
                                                               api_post=True))
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_filter_males(self):
        Utilities.sample_profile(self.user, gender='m')
        Utilities.sample_profile(self.user2, gender='f')
        Utilities.sample_profile(self.user3, gender='m')

        res = self.client.get(f"{Utilities.PROFILES_URL}?gender=m")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_filter_weight_range(self):
        Utilities.sample_profile(self.user, weight=65)
        Utilities.sample_profile(self.user2, weight=100)
        Utilities.sample_profile(self.user3, weight=80)

        res = self.client.get(
            f"{Utilities.PROFILES_URL}?min_weight=60&max_weight=80")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_filter_age(self):
        today = datetime.date.today()
        # Age 25 years
        dob1 = today - datetime.timedelta(days=25 * 360)
        # Age 32 years
        dob2 = today - datetime.timedelta(days=32 * 360)
        # Age 27 years
        dob3 = today - datetime.timedelta(days=27 * 360)

        Utilities.sample_profile(self.user, dob=dob1)
        Utilities.sample_profile(self.user2, dob=dob2)
        Utilities.sample_profile(self.user3, dob=dob3)

        res = self.client.get(
            f"{Utilities.PROFILES_URL}?min_age=24&max_age=30")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_filter_marital_status(self):
        marital_status1 = models.MaritalStatus.objects.create(
            name="Never Married"
        )

        marital_status2 = models.MaritalStatus.objects.create(
            name="Divorced"
        )

        Utilities.sample_profile(self.user, marital_status=marital_status1)
        Utilities.sample_profile(self.user2, marital_status=marital_status2)
        Utilities.sample_profile(self.user3, marital_status=marital_status1)

        res = self.client.get(
            f"{Utilities.PROFILES_URL}?marital_status={marital_status1.id}")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
