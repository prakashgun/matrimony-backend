from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from . import models


class ModelTests(TestCase):

    def setUp(self):
        self.marital_status = models.MaritalStatus.objects.create(
            name="Never Married"
        )
        self.language = models.Language.objects.create(
            name="Malayalam"
        )
        self.language2 = models.Language.objects.create(
            name="English"
        )
        self.physical_status = models.PhysicalStatus.objects.create(
            name="Normal"
        )
        self.body_type = models.BodyType.objects.create(
            name="Slim"
        )
        self.complexion = models.Complexion.objects.create(
            name="Fair"
        )
        self.created_by = models.CreatedBy.objects.create(
            name="Self"
        )
        self.eating_habit = models.EatingHabit.objects.create(
            name="Vegetarian"
        )
        self.drinking_habit = models.DrinkingHabit.objects.create(
            name="Non Drinker"
        )
        self.smoking_habit = models.SmokingHabit.objects.create(
            name="Non Smoker"
        )
        self.religion = models.Religion.objects.create(
            name="Hindu"
        )
        self.caste = models.Caste.objects.create(
            religion=self.religion,
            name="Ezhava"
        )
        self.star = models.Star.objects.create(
            name="Aswathi"
        )
        self.raasi = models.Raasi.objects.create(
            name="Medam"
        )
        self.dosham = models.Dosham.objects.create(
            name="No"
        )
        self.education = models.Education.objects.create(
            name="BE"
        )
        self.occupation = models.Occupation.objects.create(
            name="Software Professional"
        )
        self.employed_in = models.EmployedIn.objects.create(
            name="Private"
        )
        self.currency_type = models.CurrencyType.objects.create(
            name="Rs."
        )
        self.country = models.Country.objects.create(
            name="India"
        )
        self.state = models.State.objects.create(
            country=self.country,
            name="Tamil Nadu"
        )
        self.city = models.City.objects.create(
            state=self.state,
            name="Coimbatore"
        )
        self.family_value = models.FamilyValue.objects.create(
            name="Liberal"
        )
        self.family_type = models.FamilyType.objects.create(
            name="Nuclear Family"
        )
        self.family_status = models.FamilyStatus.objects.create(
            name="Middle Class"
        )

    def test_marital_status_str(self):
        self.assertEqual(str(self.marital_status), self.marital_status.name)

    def test_language_str(self):
        self.assertEqual(str(self.language), self.language.name)

    def test_physical_status_str(self):
        self.assertEqual(str(self.physical_status), self.physical_status.name)

    def test_body_type_str(self):
        self.assertEqual(str(self.body_type), self.body_type.name)

    def test_complexion_str(self):
        self.assertEqual(str(self.complexion), self.complexion.name)

    def test_created_by_str(self):
        self.assertEqual(str(self.created_by), self.created_by.name)

    def test_eating_habit_str(self):
        self.assertEqual(str(self.eating_habit), self.eating_habit.name)

    def test_drinking_habit_str(self):
        self.assertEqual(str(self.drinking_habit), self.drinking_habit.name)

    def test_smoking_habit_str(self):
        self.assertEqual(str(self.smoking_habit), self.smoking_habit.name)

    def test_religion_str(self):
        self.assertEqual(str(self.religion), self.religion.name)

    def test_caste_str(self):
        self.assertEqual(str(self.caste), self.caste.name)

    def test_star_str(self):
        self.assertEqual(str(self.star), self.star.name)

    def test_raasi_str(self):
        self.assertEqual(str(self.raasi), self.raasi.name)

    def test_dosham_str(self):
        self.assertEqual(str(self.dosham), self.dosham.name)

    def test_education_str(self):
        self.assertEqual(str(self.education), self.education.name)

    def test_occupation_str(self):
        self.assertEqual(str(self.occupation), self.occupation.name)

    def test_employed_in_str(self):
        self.assertEqual(str(self.employed_in), self.employed_in.name)

    def test_currency_type_str(self):
        self.assertEqual(str(self.currency_type), self.currency_type.name)

    def test_country_str(self):
        self.assertEqual(str(self.country), self.country.name)

    def test_state_str(self):
        self.assertEqual(str(self.state), self.state.name)

    def test_city_str(self):
        self.assertEqual(str(self.city), self.city.name)

    def test_family_value_str(self):
        self.assertEqual(str(self.family_value), self.family_value.name)

    def test_family_type_str(self):
        self.assertEqual(str(self.family_type), self.family_type.name)

    def test_family_status_str(self):
        self.assertEqual(str(self.family_status), self.family_status.name)

    def test_profile_str(self):
        profile = models.Profile.objects.create(
            user=get_user_model().objects.create(
                username='9876543210', password='test',
                email='test@example.com'
            ),
            dob=datetime.strptime('1995-08-11', '%Y-%m-%d').date(),
            about='Software Engineer working in Bangalore',
            height=182,
            weight=70,
            marital_status=self.marital_status,
            mother_tongue=self.language,
            physical_status=self.physical_status,
            created_by=self.created_by,
            eating_habit=self.eating_habit,
            drinking_habit=self.drinking_habit,
            smoking_habit=self.smoking_habit,
            education=self.education,
            education_institution='CMS College of Science and Commerce',
            occupation=self.occupation,
            occupation_in_detail='Software Programmer',
            organization='Spi Global',
            employed_in=self.employed_in,
            currency_type=self.currency_type,
            annual_income=10,
            country=self.country,
            state=self.state,
            city=self.city,
            citizenship=self.country,
            family_value=self.family_value,
            family_type=self.family_type,
            family_status=self.family_status,
            father_occupation=self.occupation,
            mother_occupation=self.occupation,
            no_of_brothers=1,
            brothers_married=None,
            no_of_sisters=1,
            sisters_married=None,
            ancestral_origin='Parsi',
            about_family='Middle class family staying in Bangalore'
        )

        profile.spoken_languages.set([self.language, self.language2])

        self.assertEqual(str(profile), profile.about)
