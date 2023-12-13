from django.contrib import admin

from users.models import UserModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number',
                    'is_phone_number_verified', 'created_at', 'updated_at',)
    list_display_links = ('id', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('updated_at',)
