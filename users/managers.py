from typing import Any, Type
from django.db import models


from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class UserQuerySet(models.query.QuerySet):
    def search(self, query: str) -> Type['UserQuerySet']:
        lookups = (
            models.Q(phone_number__contains=query) |
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query)
        )
        return self.filter(lookups).distinct()


class UserModelManager(BaseUserManager):
    phone = PhoneNumberField
    use_in_migrations = True

    def get_queryset(self) -> UserQuerySet:
        return UserQuerySet(self.model, using=self._db)

    def search(self, query: str) -> Type['UserQuerySet']:
        return self.get_queryset().search(query)

    def _create_user(self, phone_number: str, password: Any = None, **extra_fields: dict) -> Type['UserModel']:
        """
        Create and save a user with the given phone.
        """
        if not phone_number:
            raise ValueError('The given phone must be set')

        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, phone_number: str, **extra_fields: Any) -> Type['UserModel']:
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, **extra_fields)

    def create_superuser(self, phone_number: str, password: Any, **extra_fields: Any) -> Type['UserModel']:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)


class TrainerManager(UserModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_trainer=True)


class StudentManager(UserModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_trainer=False)
