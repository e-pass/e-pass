from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import SectionModel, GroupModel


@admin.register(SectionModel)
class SectionAdmin(ModelAdmin):
    pass


@admin.register(GroupModel)
class SectionGroupAdmin(ModelAdmin):
    pass
