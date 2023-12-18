from typing import Any, Optional, Type

from django.db import models
from django.utils import timezone

from ePass import settings
from users.models import UserModel


class ConfirmationCodeModel(models.Model):
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args: Any, **kwargs: dict) -> None:
        self.expires_at = timezone.now() + timezone.timedelta(minutes=settings.CONFIRMATION_CODE_EXPIRATION)
        super().save(*args, **kwargs)

    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at

    def mark_code_as_used(self) -> None:
        self.is_valid = False
        self.user.is_phone_number_verified = True
        self.user.save()
        self.save()

    @classmethod
    def get_confirmation_code(cls: Type['ConfirmationCodeModel'], code: str) -> Optional['ConfirmationCodeModel']:
        try:
            return cls.objects.get(code=code)
        except cls.DoesNotExist:
            return None
