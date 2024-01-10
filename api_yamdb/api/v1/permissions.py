from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminSuperuserChangeOrAnyReadOnly(BasePermission):
    """Admin and SuperUser can edit, other users read only."""

    def has_permission(self, request, view):
        user = request.user
        is_admin = getattr(user, 'is_admin', False)
        return (is_admin or user.is_superuser
                or request.method in SAFE_METHODS)


class OwnerModeratorChange(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.method in SAFE_METHODS
            or user == obj.author
            or user.is_moderator or user.is_admin)
