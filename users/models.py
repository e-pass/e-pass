from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import EmailValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import StudentManager, TrainerManager, UserModelManager


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

    student_parent_name = models.CharField(max_length=255, blank=True, null=True)
    student_parent_phone = PhoneNumberField(region=settings.PHONE_NUMBER_REGION, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(editable=False, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('first_name', 'last_name',)

    objects = UserModelManager()
    trainers = TrainerManager()
    students = StudentManager()

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}, {self.phone_number}'
