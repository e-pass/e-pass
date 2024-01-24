from django.contrib import admin

from membership_passes.models import PassModel


@admin.register(PassModel)
class PassModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'valid_from', 'valid_until', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'student')
    filter_horizontal = ('lessons',)
    readonly_fields = ('quantity_unused_lessons',)
    fieldsets = (
        ('Main info', {
            'fields': ('name', 'student', 'section', 'qr_code')
        }),
        ('Lessons data', {
            'fields': ('is_unlimited', 'quantity_lessons_max', 'quantity_unused_lessons', 'lessons'),
        }),
        ('Validity', {
            'fields': ('is_active', 'valid_from', 'valid_until')
        }),
        ('Other', {
            'fields': ('price', 'is_paid')
        })
    )
