from rest_framework.permissions import BasePermission

from .models import CustomUser


class IsAdminOrSuperuser(BasePermission):
    """Admin and SuperUser can edit, other users not allowed."""

    def has_permission(self, request, view):
        role = getattr(request.user, 'role', 'anon')
        return (request.user.is_superuser or role == CustomUser.Role.ADMIN)
