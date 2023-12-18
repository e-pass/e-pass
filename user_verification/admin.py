from django.contrib import admin

from user_verification.models import ConfirmationCodeModel


@admin.register(ConfirmationCodeModel)
class ConfirmationCodeModelAdmin(admin.ModelAdmin):
    ordering = ('id', 'user',)
