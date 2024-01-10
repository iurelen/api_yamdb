from rest_framework.permissions import BasePermission

# from .models import CustomUser


class IsAdminOrSuperuser(BasePermission):
    """Admin and SuperUser can edit, other users not allowed."""

    def has_permission(self, request, view):
        is_admin = getattr(request.user, 'is_admin', False)
        return request.user.is_superuser or is_admin
