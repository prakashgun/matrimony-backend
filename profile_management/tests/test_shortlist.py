from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .sample_data import Utilities


class PublicShortlistTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_shortlist_unauthenticated(self):
        res = self.client.get(Utilities.SHORTLISTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateShortlistTests(TestCase):

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

    def test_shortlist_addition(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id
        }
        res = self.client.post(Utilities.SHORTLISTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_shortlist_cannot_be_added_more_than_once(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id
        }
        res = self.client.post(Utilities.SHORTLISTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id
        }
        res = self.client.post(Utilities.SHORTLISTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_own_shortlists_can_be_seen(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
        }
        res = self.client.post(Utilities.SHORTLISTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(Utilities.SHORTLISTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['to_profile'], profile2.id)

        self.client.force_authenticate(profile2.user)
        res = self.client.get(Utilities.SHORTLISTS_URL)
        self.assertEqual(len(res.data), 0)

    def test_only_own_shortlist_detail_can_be_seen(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
        }
        res = self.client.post(Utilities.SHORTLISTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(Utilities.shortlist_detail_url(res.data['id']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(profile2.user)
        res = self.client.get(Utilities.shortlist_detail_url(res.data['id']))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_own_shortlist_can_be_deleted(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
        }
        res = self.client.post(Utilities.SHORTLISTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        shortlist_id = res.data['id']
        res = self.client.delete(
            Utilities.shortlist_detail_url(shortlist_id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        res = self.client.get(
            Utilities.shortlist_detail_url(shortlist_id=shortlist_id))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
