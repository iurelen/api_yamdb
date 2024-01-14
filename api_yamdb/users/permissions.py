from rest_framework.permissions import BasePermission


class IsAdminOrSuperuser(BasePermission):
    """Admin and SuperUser can edit, other users not allowed."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_superuser or request.user.is_admin))
