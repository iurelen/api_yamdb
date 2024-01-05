from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        role = getattr(request.user, 'role', 'anon')
        return role == 'admin' or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or request.user.is_superuser
