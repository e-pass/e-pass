from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserModel(AbstractUser):
    phone_number = PhoneNumberField(null=False, blank=True, unique=True)
    is_phone_number_verified = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
