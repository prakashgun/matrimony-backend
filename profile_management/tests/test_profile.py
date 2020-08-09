from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .. import models
from .. import serializers


class Utilities:
    PROFILES_URL = reverse('profile_management:profile-list')

    @staticmethod
    def create_user(**params):
        return get_user_model().objects.create(**params)

    @staticmethod
    def sample_user():
        return Utilities.create_user(username='9876543210', password='test',
                                     email='test@example.com')

    @staticmethod
    def sample_profile(user, **params):
        marital_status = models.MaritalStatus.objects.create(
            name="Never Married"
        )
        language = models.Language.objects.create(
            name="Malayalam"
        )
        language2 = models.Language.objects.create(
            name="English"
        )
        physical_status = models.PhysicalStatus.objects.create(
            name="Normal"
        )
        body_type = models.BodyType.objects.create(
            name="Slim"
        )
        complexion = models.Complexion.objects.create(
            name="Fair"
        )
        created_by = models.CreatedBy.objects.create(
            name="Self"
        )
        eating_habit = models.EatingHabit.objects.create(
            name="Vegetarian"
        )
        drinking_habit = models.DrinkingHabit.objects.create(
            name="Non Drinker"
        )
        smoking_habit = models.SmokingHabit.objects.create(
            name="Non Smoker"
        )
        religion = models.Religion.objects.create(
            name="Hindu"
        )
        caste = models.Caste.objects.create(
            religion=religion,
            name="Ezhava"
        )
        star = models.Star.objects.create(
            name="Aswathi"
        )
        raasi = models.Raasi.objects.create(
            name="Medam"
        )
        dosham = models.Dosham.objects.create(
            name="No"
        )
        education = models.Education.objects.create(
            name="BE"
        )
        occupation = models.Occupation.objects.create(
            name="Software Professional"
        )
        employed_in = models.EmployedIn.objects.create(
            name="Private"
        )
        currency_type = models.CurrencyType.objects.create(
            name="Rs."
        )
        country = models.Country.objects.create(
            name="India"
        )
        state = models.State.objects.create(
            country=country,
            name="Tamil Nadu"
        )
        city = models.City.objects.create(
            state=state,
            name="Coimbatore"
        )
        family_value = models.FamilyValue.objects.create(
            name="Liberal"
        )
        family_type = models.FamilyType.objects.create(
            name="Nuclear Family"
        )
        family_status = models.FamilyStatus.objects.create(
            name="Middle Class"
        )
        defaults = {
            "dob": datetime.strptime('1995-08-11', '%Y-%m-%d').date(),
            "about": 'Software Engineer working in Bangalore',
            "height": 182,
            "weight": 70,
            "marital_status": marital_status,
            "mother_tongue": language,
            "physical_status": physical_status,
            "body_type": body_type,
            "complexion": complexion,
            "created_by": created_by,
            "eating_habit": eating_habit,
            "drinking_habit": drinking_habit,
            "smoking_habit": smoking_habit,
            "religion": religion,
            "caste": caste,
            "star": star,
            "raasi": raasi,
            "dosham": dosham,
            "education": education,
            "education_institution": 'CMS College of Science and Commerce',
            "occupation": occupation,
            "occupation_in_detail": 'Software Programmer',
            "organization": 'Spi Global',
            "employed_in": employed_in,
            "currency_type": currency_type,
            "annual_income": 10,
            "country": country,
            "state": state,
            "city": city,
            "citizenship": country,
            "family_value": family_value,
            "family_type": family_type,
            "family_status": family_status,
            "father_occupation": occupation,
            "mother_occupation": occupation,
            "no_of_brothers": 1,
            "brothers_married": None,
            "no_of_sisters": 1,
            "sisters_married": None,
            "ancestral_origin": 'Parsi',
            "about_family": 'Middle class family staying in Bangalore'
        }

        defaults.update(params)

        profile = models.Profile.objects.create(user=user, **defaults)
        profile.spoken_languages.set([language, language2])

        return profile


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

        self.user2 = get_user_model().objects.create_user(
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
