from django.views import View
from rest_framework import permissions
from rest_framework.request import Request


class IsTrainer(permissions.BasePermission):

    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated and request.user.is_trainer


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.id
