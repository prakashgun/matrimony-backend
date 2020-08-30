from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .sample_data import Utilities


class PublicInterestTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_interest_unauthenticated(self):
        res = self.client.get(Utilities.INTERESTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateInterestTests(TestCase):

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

        self.user4 = Utilities.sample_user(
            username='1234511111',
            password='test4',
            email='test4@example.com'
        )
        self.client.force_authenticate(self.user)

    def test_interest_addition(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "s"
        }
        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_interest_cannot_be_added_more_than_once(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "s"
        }
        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "s"
        }
        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_interest_receiver_can_accept_request(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "s"
        }
        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "a"
        }
        self.client.force_authenticate(profile2.user)
        res = self.client.put(Utilities.interest_detail_url(res.data['id']),
                              data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_interest_receiver_cannot_change_sender(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        profile4 = Utilities.sample_profile(self.user4, gender='m')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "s"
        }
        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        interest_id = res.data['id']

        accept_payload = {
            "from_profile": profile4.id,
            "to_profile": profile2.id,
            "status": "a"
        }
        self.client.force_authenticate(profile2.user)
        res = self.client.put(
            Utilities.interest_detail_url(interest_id=interest_id),
            data=accept_payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get(
            Utilities.interest_detail_url(interest_id=interest_id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                'id': interest_id,
                'from_profile': payload['from_profile'],
                'to_profile': payload['to_profile'],
                'status': accept_payload['status']
            }
        )

    def test_interest_sender_can_delete(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "s"
        }
        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        interest_id = res.data['id']

        res = self.client.delete(
            Utilities.interest_detail_url(interest_id=interest_id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_interest_receiver_can_reject_request(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "s"
        }
        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "r"
        }
        self.client.force_authenticate(profile2.user)
        res = self.client.put(Utilities.interest_detail_url(res.data['id']),
                              data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], payload['status'])

    def test_interest_receiver_can_only_accept_request(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "s"
        }
        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "a"
        }
        res = self.client.put(Utilities.interest_detail_url(res.data['id']),
                              data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_related_interest_detail_can_be_seen(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        profile3 = Utilities.sample_profile(self.user3, gender='f')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "s"
        }
        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(profile2.user)
        res = self.client.get(Utilities.interest_detail_url(res.data['id']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(profile3.user)
        res = self.client.get(Utilities.interest_detail_url(res.data['id']))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_only_related_interests_list_can_be_seen(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        profile3 = Utilities.sample_profile(self.user3, gender='f')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            'status': 's'
        }
        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(Utilities.INTERESTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['to_profile'], profile2.id)

        self.client.force_authenticate(profile2.user)
        res = self.client.get(Utilities.INTERESTS_URL)
        self.assertEqual(len(res.data), 1)

        self.client.force_authenticate(profile3.user)
        res = self.client.get(Utilities.INTERESTS_URL)
        self.assertEqual(len(res.data), 0)

    def test_sent_interests_list(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        profile3 = Utilities.sample_profile(self.user3, gender='f')
        profile4 = Utilities.sample_profile(self.user4, gender='m')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "s"
        }
        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        payload = {
            "from_profile": profile.id,
            "to_profile": profile3.id,
            "status": "s"
        }
        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        payload = {
            "from_profile": profile3.id,
            "to_profile": profile4.id,
            "status": "s"
        }
        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(Utilities.INTERESTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_accepted_interests_list(self):
        profile = Utilities.sample_profile(self.user, gender='m')
        profile2 = Utilities.sample_profile(self.user2, gender='f')
        profile3 = Utilities.sample_profile(self.user3, gender='f')
        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "s"
        }
        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        payload = {
            "from_profile": profile.id,
            "to_profile": profile2.id,
            "status": "a"
        }
        self.client.force_authenticate(profile2.user)
        res = self.client.put(Utilities.interest_detail_url(res.data['id']),
                              data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        payload = {
            "from_profile": profile.id,
            "to_profile": profile3.id,
            "status": "s"
        }
        self.client.force_authenticate(profile.user)

        res = self.client.post(Utilities.INTERESTS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(f"{Utilities.INTERESTS_URL}?status=a")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
