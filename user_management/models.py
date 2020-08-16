from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(unique=True, validators=[])
    first_name = models.CharField(_('first name'), max_length=30, blank=False,
                                  null=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False,
                                 null=False)
