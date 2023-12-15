from django.contrib import admin

from authentication.models import ConfirmationCodeModel


@admin.register(ConfirmationCodeModel)
class ConfirmationCodeModelAdmin(admin.ModelAdmin):
    ordering = ('id', 'user',)
