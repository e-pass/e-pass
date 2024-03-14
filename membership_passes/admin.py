import datetime
from typing import Any

from django import forms
from django.contrib import admin
from django.db.models import Field
from django.http import HttpRequest

from membership_passes.models import EntryModel, PassModel
from users.models import UserModel


class PassModelAdminForm(forms.ModelForm):
    class Meta:
        model = PassModel
        fields = '__all__'

    def clean(self) -> Any:
        cleaned_data = super().clean()
        valid_from = cleaned_data.get('valid_from')
        valid_until = cleaned_data.get('valid_until')
        if valid_from and valid_until:
            if valid_from > valid_until:
                raise forms.ValidationError('Введён некорректный период действия')
            if valid_until < datetime.date.today():
                raise forms.ValidationError('Введённая дата окончания срока действия в прошлом')
        return cleaned_data


@admin.register(PassModel)
class PassModelAdmin(admin.ModelAdmin):
    form = PassModelAdminForm
    list_display = ('id', 'name', 'student', 'valid_from', 'valid_until', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'name', 'student')
    readonly_fields = ('quantity_unused_lessons',)
    fieldsets = (
        ('Main info', {
            'fields': ('name', 'student', 'section')
        }),
        ('Lessons data', {
            'fields': ('quantity_lessons_max', 'quantity_unused_lessons'),
        }),
        ('Validity', {
            'fields': ('is_active', 'valid_from', 'valid_until')
        }),
        ('Other', {
            'fields': ('price', 'is_paid')
        })
    )

    def quantity_unused_lessons(self, obj: PassModel) -> int:
        return obj.quantity_lessons_max - obj.entries.count()

    def formfield_for_foreignkey(
            self, db_field: Field, request: HttpRequest, **kwargs: dict[Any, Any]) -> forms.ModelChoiceField:
        """Функция для создания списка студентов для выбора"""
        if db_field.name == 'student':
            kwargs['queryset'] = UserModel.students.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(EntryModel)
class EntryModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
