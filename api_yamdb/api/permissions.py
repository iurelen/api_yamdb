from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminSuperuserChangeOrAnyReadOnly(BasePermission):
    """Admin and SuperUser can edit, oteher users read only."""

    def has_permission(self, request, view):
        role = getattr(request.user, 'role', 'anon')
        return (request.method in SAFE_METHODS
                or role == 'admin' or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class OwnerModeratorChange(BasePermission):
    def has_object_permission(self, request, view, obj):
        role = getattr(request.user, 'role', 'anon')
        return (request.user == obj.author
                or role == 'moderator')
