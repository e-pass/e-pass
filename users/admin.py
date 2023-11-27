from django.contrib import admin

from users.models import UserModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone_number', 'is_phone_number_verified', 'date_joined', 'updated_at',)
    readonly_fields = ('updated_at',)
