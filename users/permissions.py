from typing import Any

from django.views import View
from rest_framework import permissions
from rest_framework.request import Request


class IsTrainer(permissions.BasePermission):

    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_trainer


class IsOwnerOrStaff(permissions.BasePermission):

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        return any((obj.owner == request.user,
                    request.user.is_staff))


class IsSectionOwnerOrGroupTrainerOrStaff(permissions.BasePermission):

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        return any((obj.section.owner == request.user,
                    obj.trainer == request.user,
                    request.user.is_staff))
