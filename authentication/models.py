from typing import Any

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
        return False if timezone.now() <= self.expires_at else True

    class Meta:
        unique_together = ('user', 'code',)
