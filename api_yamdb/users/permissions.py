from rest_framework.permissions import BasePermission


class IsAdminOrSuperuser(BasePermission):
    """Admin and SuperUser can edit, other users not allowed."""

    def has_permission(self, request, view):
        role = getattr(request.user, 'role', 'anon')
        return role == 'admin' or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
