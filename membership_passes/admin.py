from django.contrib import admin
from django.contrib.admin import ModelAdmin

from membership_passes.models import PassModel


@admin.register(PassModel)
class PassModelAdmin(ModelAdmin):
    list_display = ('id', 'student', 'section', 'group', 'valid_until', 'is_active')
    list_display_links = ('id', 'student')


