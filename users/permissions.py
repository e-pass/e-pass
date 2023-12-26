from typing import Any

from django.views import View
from rest_framework import permissions
from rest_framework.request import Request


class IsOwnerOrStaff(permissions.BasePermission):
    """Права на аккаунт для владельца аккаунта или администратора"""

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        return any((obj.id == request.user.id, request.user.is_staff))


class IsSectionOwnerOrGroupTrainerOrAccountOwnerOrStaff(permissions.BasePermission):
    """Права на аккаунт для владельца секции(если аккаунт подписан к секции),
        тренеров групп(если аккаунт подписан к группам),
        владельца аккаунта или администратора"""

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        section_owners, group_trainers = [], []
        if obj.section:
            section_owners = [section.owner.id for section in obj.section.all()]
        if obj.my_groups:
            group_trainers = [group.trainer.id for group in obj.my_groups.all()]
        return any((
            request.user.id in section_owners,
            request.user.id in group_trainers,
            obj.id == request.user.id, request.user.is_staff
        ))
