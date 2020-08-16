from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class Utilities:
    USERS_URL = reverse('user_management:users')
    GROUPS_URL = reverse('user_management:groups')

    @staticmethod
    def create_user(**params):
        return get_user_model().objects.create(**params)

    @staticmethod
    def sample_user():
        return Utilities.create_user(username='9876543210', password='test',
                                     email='test@example.com')


class ModelTests(TestCase):

    def test_create_user_successful(self):
        username = '9876543210'
        password = 'test'
        email = 'test@example.com'

        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            email=email
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


class UserPublicApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test create user with payload"""
        payload = {
            'username': '9876543210',
            'password': 'test',
            'email': 'test@example.com'
        }

        res = self.client.post(Utilities.USERS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_unique_email(self):
        """Test user cannot be created with already existing email"""
        payload = {
            'username': '9876543210',
            'password': 'test',
            'email': 'test@example.com'
        }

        Utilities.create_user(**payload)

        payload = {
            'username': '9976543210',
            'password': 'test2',
            'email': 'test@example.com'
        }

        res = self.client.post(Utilities.USERS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_username(self):
        """Validate that username is ten digit"""
        payload = {
            'username': '',
            'password': 'test',
            'email': 'test@example.com'
        }

        res = self.client.post(Utilities.USERS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_email(self):
        """Validate that username is ten digit"""
        payload = {
            'username': '9876543210',
            'password': 'test',
            'email': 'wrong_email'
        }

        res = self.client.post(Utilities.USERS_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class UserPrivateApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = Utilities.sample_user()
        self.client.force_authenticate(self.user)

    def test_list_users(self):
        """Test listing of users"""
        res = self.client.get(Utilities.USERS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, res.data[0]['username'])

    def test_list_groups(self):
        """Test listing of user groups"""
        group1 = Group.objects.create(name="Group 1")
        group2 = Group.objects.create(name="Group 2")

        res = self.client.get(Utilities.GROUPS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['name'], group1.name)
        self.assertEqual(res.data[1]['name'], group2.name)

    def test_user_detail(self):
        """Test individual user detail retrieving"""
        res = self.client.get(
            reverse('user_management:user_detail', args=(self.user.id,))
        )
        self.assertEqual(res.data['username'], self.user.username)
