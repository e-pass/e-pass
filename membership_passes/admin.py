from django.contrib import admin
from django.db.models import Count

from membership_passes.models import PassModel, EntryModel


@admin.register(PassModel)
class PassModelAdmin(admin.ModelAdmin):
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

    def quantity_unused_lessons(self, obj):
        result = 0
        if not obj.is_unlimited:
            result = obj.quantity_lessons_max - obj.entries.count()
        return result

@admin.register(EntryModel)
class EntryModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
