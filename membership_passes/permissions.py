from typing import Type

from django.views import View
from rest_framework import permissions
from rest_framework.request import Request


class IsTrainer(permissions.BasePermission):
    """Простая проверка, является ли пользователь тренером"""
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_trainer


class IsPassStudentOrTrainerOrSectionOwner(permissions.BasePermission):
    """Права на абонемент для студента, тренера или владельца секции"""

    def has_object_permission(self, request: Request, view: View, obj: Type['PassModel'])-> bool:
        return any((request.user == obj.student, request.user in obj.section.trainers.all(),
                    request.user == obj.section.owner))


class IsTrainerOrSectionOwner(permissions.BasePermission):
    """Права на абонемент для тренера или владельца секции"""

    def has_object_permission(self, request: Request, view: View, obj: Type['PassModel']) -> bool:
        return any((request.user in obj.section.trainers.all(),
                    request.user == obj.section.owner))
