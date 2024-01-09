import logging

from rest_framework.permissions import BasePermission, SAFE_METHODS

logging.basicConfig(level=logging.DEBUG)

class AdminSuperuserChangeOrAnyReadOnly(BasePermission):
    """Admin and SuperUser can edit, other users read only."""
    def has_permission(self, request, view):
        is_admin = getattr(request.user, 'is_admin', False)
        return (is_admin or request.user.is_superuser
                or request.method in SAFE_METHODS)

class OwnerModeratorChange(AdminSuperuserChangeOrAnyReadOnly):
    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                or request.user.is_authenticated
                or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (super().has_permission(request, view)
                or request.method in SAFE_METHODS
                or request.user == obj.author
                or request.user.is_moderator)
