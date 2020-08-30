from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class MaritalStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class PhysicalStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class BodyType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Complexion(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class CreatedBy(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class EatingHabit(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class DrinkingHabit(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class SmokingHabit(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Religion(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Caste(models.Model):
    name = models.CharField(max_length=255, unique=True)
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Star(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Raasi(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Dosham(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Education(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Occupation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class EmployedIn(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class CurrencyType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255, unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.name


class FamilyValue(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class FamilyType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class FamilyStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Profile(models.Model):
    """All information about user other than authentication"""
    objects = models.Manager()
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    dob = models.DateField()
    about = models.TextField()
    height = models.IntegerField()
    weight = models.IntegerField()
    gender = models.CharField(max_length=1,
                              choices=(('m', _('Male')), ('f', _('Female'))),
                              blank=False, null=False)
    marital_status = models.ForeignKey(
        MaritalStatus, on_delete=models.CASCADE,
        related_name='marital_status_profile_set')
    mother_tongue = models.ForeignKey(
        Language, on_delete=models.CASCADE,
        related_name='mother_tongue_profile_set')
    physical_status = models.ForeignKey(
        PhysicalStatus,
        on_delete=models.CASCADE,
        related_name='physical_status_profile_set')
    created_by = models.ForeignKey(
        CreatedBy, on_delete=models.CASCADE,
        related_name='created_by_profile_set')
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE,
        related_name='country_profile_set')
    state = models.ForeignKey(
        State, on_delete=models.CASCADE,
        related_name='state_profile_set')
    city = models.ForeignKey(
        City, on_delete=models.CASCADE,
        related_name='city_profile_set')
    citizenship = models.ForeignKey(
        Country, on_delete=models.CASCADE,
        related_name='citizenship_profile_set')
    body_type = models.ForeignKey(
        BodyType,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='body_type_profile_set')
    complexion = models.ForeignKey(
        Complexion,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='complexion_profile_set')
    eating_habit = models.ForeignKey(
        EatingHabit, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='eating_habit_profile_set')
    drinking_habit = models.ForeignKey(
        DrinkingHabit, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='drinking_habit_profile_set')
    smoking_habit = models.ForeignKey(
        SmokingHabit, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='smoking_habit_profile_set')
    religion = models.ForeignKey(
        Religion, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='religion_profile_set')
    caste = models.ForeignKey(
        Caste, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='caste_profile_set')
    star = models.ForeignKey(
        Star, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='star_profile_set')
    raasi = models.ForeignKey(
        Raasi, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='raasi_profile_set')
    dosham = models.ForeignKey(
        Dosham, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='dosham_profile_set')
    education = models.ForeignKey(
        Education, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='education_profile_set')
    education_institution = models.CharField(max_length=255, blank=True,
                                             null=True)
    occupation = models.ForeignKey(
        Occupation, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='occupation_profile_set')
    occupation_in_detail = models.CharField(max_length=255, blank=True,
                                            null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    employed_in = models.ForeignKey(
        EmployedIn, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='employed_in_profile_set')
    currency_type = models.ForeignKey(
        CurrencyType, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='currency_type_profile_set')
    annual_income = models.IntegerField(blank=True, null=True)
    family_value = models.ForeignKey(
        FamilyValue, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='family_value_profile_set')
    family_type = models.ForeignKey(
        FamilyType, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='family_type_profile_set')
    family_status = models.ForeignKey(
        FamilyStatus, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='family_status_profile_set')
    father_occupation = models.ForeignKey(
        Occupation, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='father_occupation_profile_set')
    mother_occupation = models.ForeignKey(
        Occupation, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='mother_occupation_profile_set')
    no_of_brothers = models.IntegerField(blank=True, null=True)
    brothers_married = models.IntegerField(blank=True, null=True)
    no_of_sisters = models.IntegerField(blank=True, null=True)
    sisters_married = models.IntegerField(blank=True, null=True)
    ancestral_origin = models.CharField(max_length=255, blank=True, null=True)
    about_family = models.TextField(blank=True, null=True)
    spoken_languages = models.ManyToManyField(
        Language, blank=True, related_name='spoken_languages_profile_set')

    def __str__(self):
        return self.about


class Interest(models.Model):
    objects = models.Manager()
    from_profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                     related_name='from_profile_profile_set')
    to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                   related_name='to_profile_profile_set')
    status = models.CharField(max_length=1,
                              choices=(
                                  ('s', _('Sent')),
                                  ('a', _('Accepted')),
                                  ('r', _('Rejected'))
                              ),
                              blank=False, null=False)

    class Meta:
        unique_together = ('from_profile', 'to_profile')

    def __str__(self):
        return f"{self.from_profile}-{self.to_profile}-{self.status}"


class Shortlist(models.Model):
    objects = models.Manager()
    from_profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                     related_name='from_profile_shortlist_set')
    to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                   related_name='to_profile_shortlist_set')

    class Meta:
        unique_together = ('from_profile', 'to_profile')

    def __str__(self):
        return f"{self.from_profile}-{self.to_profile}"
