from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class UserModelManager(BaseUserManager):
    phone = PhoneNumberField
    use_in_migrations = True

    def _create_user(self, phone_number, password=None, **extra_fields):
        """
        Create and save a user with the given phone.
        """
        if not phone_number:
            raise ValueError("The given phone must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, phone_number, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)
