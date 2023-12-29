from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import GroupModel, SectionModel


@admin.register(SectionModel)
class SectionAdmin(ModelAdmin):
    pass


@admin.register(GroupModel)
class GroupAdmin(ModelAdmin):
    pass
