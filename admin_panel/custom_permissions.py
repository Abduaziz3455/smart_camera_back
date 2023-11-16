from datetime import datetime

from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_superuser)


class IsExpired(BasePermission):
    def has_permission(self, request, view):
        return request.user.organization.subscription_ends_date > datetime.today().date()
