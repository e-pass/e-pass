from typing import Any

from django.views import View
from rest_framework import permissions
from rest_framework.request import Request

from users.models import TrainerModel


class IsOwnerOrStaff(permissions.BasePermission):
    """Права на аккаунт для владельца аккаунта или администратора"""

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        return any((obj.id == request.user.id, request.user.is_staff))


class IsSectionOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        return request.user.id == obj.owner_id


class IsGroupTrainerOrAccountOwnerOrStaff(permissions.BasePermission):
    """Права на аккаунт для владельца секции(если аккаунт подписан к секции),
        тренеров групп(если аккаунт подписан к группам),
        владельца аккаунта или администратора"""

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        group_trainers = []
        if obj.my_groups:
            group_trainers = [group.trainer.id for group in obj.my_groups.all()]
        return any((
            request.user.id in group_trainers,
            obj.id == request.user.id, request.user.is_staff
        ))


class IsTrainer(permissions.BasePermission):
    """Проверка, является ли пользователь тренером"""

    def has_permission(self, request: Request, view: View) -> bool:
        phone_number = request.user.phone_number
        return TrainerModel.objects.filter(phone_number=phone_number).exists()
