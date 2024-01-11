from rest_framework.permissions import BasePermission


class IsAdminOrSuperuser(BasePermission):
    """Admin and SuperUser can edit, other users not allowed."""

    def has_permission(self, request, view):
        is_admin = getattr(request.user, 'is_admin', False)
        return request.user.is_authenticated and is_admin
