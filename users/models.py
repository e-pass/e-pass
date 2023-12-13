from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import EmailValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserModelManager


class UserModel(AbstractBaseUser, PermissionsMixin):
    """User model"""
    phone_number = PhoneNumberField(region=settings.PHONE_NUMBER_REGION,
                                    unique=True, blank=False, null=False)
    password = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, validators=[EmailValidator])
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)

    is_trainer = models.BooleanField(default=False)
    is_phone_number_verified = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'is_trainer')

    objects = UserModelManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.phone_number}'


class OTPModel(models.Model):
    """One time password model"""
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='otp')

    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=settings.MAX_OTP_TRY)
    otp_max_out = models.DateTimeField(blank=True, null=True)
