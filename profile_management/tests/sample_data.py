from datetime import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse

from .. import models


class Utilities:
    PROFILES_URL = reverse('profile_management:profile-list')
    INTEREST_URL = reverse('profile_management:interest-list')

    @staticmethod
    def create_user(**params):
        return get_user_model().objects.create(**params)

    @staticmethod
    def sample_user(**params):
        defaults = {
            'username': '9876543210',
            'password': 'test',
            'email': 'test@exaple.com'
        }

        defaults.update(params)
        return Utilities.create_user(**defaults)

    @staticmethod
    def profile_detail_url(profile_id):
        return reverse('profile_management:profile-detail', args=[profile_id])

    @staticmethod
    def profile_defaults(user, api_post=False):
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

        return {
            "user": user.id if api_post else user,
            "dob": datetime.strptime('1995-08-11', '%Y-%m-%d').date(),
            "about": 'Software Engineer working in Bangalore',
            "height": 182,
            "weight": 70,
            "gender": "m",
            "marital_status": marital_status.id if api_post else marital_status,
            "mother_tongue": language.id if api_post else language,
            "physical_status": physical_status.id if api_post else physical_status,
            "body_type": body_type.id if api_post else body_type,
            "complexion": complexion.id if api_post else complexion,
            "created_by": created_by.id if api_post else created_by,
            "eating_habit": eating_habit.id if api_post else eating_habit,
            "drinking_habit": drinking_habit.id if api_post else drinking_habit,
            "smoking_habit": smoking_habit.id if api_post else smoking_habit,
            "religion": religion.id if api_post else religion,
            "caste": caste.id if api_post else caste,
            "star": star.id if api_post else star,
            "raasi": raasi.id if api_post else raasi,
            "dosham": dosham.id if api_post else dosham,
            "education": education.id if api_post else education,
            "education_institution": 'CMS College of Science and Commerce',
            "occupation": occupation.id if api_post else occupation,
            "occupation_in_detail": 'Software Programmer',
            "organization": 'Spi Global',
            "employed_in": employed_in.id if api_post else employed_in,
            "currency_type": currency_type.id if api_post else currency_type,
            "annual_income": 10,
            "country": country.id if api_post else country,
            "state": state.id if api_post else state,
            "city": city.id if api_post else city,
            "citizenship": country.id if api_post else country,
            "family_value": family_value.id if api_post else family_value,
            "family_type": family_type.id if api_post else family_type,
            "family_status": family_status.id if api_post else family_status,
            "father_occupation": occupation.id if api_post else occupation,
            "mother_occupation": occupation.id if api_post else occupation,
            "no_of_brothers": 1,
            "brothers_married": 0,
            "no_of_sisters": 1,
            "sisters_married": 0,
            "ancestral_origin": 'Parsi',
            "about_family": 'Middle class family staying in Bangalore',
            "spoken_languages": [language.id if api_post else language,
                                 language2.id if api_post else language2]
        }

    @staticmethod
    def sample_profile(user, **params):
        defaults = Utilities.profile_defaults(user=user)
        defaults.update(params)
        spoken_languages = defaults.pop('spoken_languages')
        profile = models.Profile.objects.create(**defaults)
        profile.spoken_languages.set(spoken_languages)
        return profile

    @staticmethod
    def sample_interest():
        user1 = Utilities.sample_user()
        user2 = Utilities.sample_user(
            username='0123456789',
            password='test2',
            email='test2@example.com'
        )
        profile1 = Utilities.sample_profile(user1, gender='m')
        profile2 = Utilities.sample_profile(user2, gender='f')
        return models.Interest.objects.create(from_profile=profile1,
                                              to_profile=profile2, status='s')
