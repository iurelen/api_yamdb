from rest_framework.permissions import BasePermission, SAFE_METHODS

class AdminSuperuserChangeOrAnyReadOnly(BasePermission):
    """
    Admin and SuperUser can edit, oteher users read only.
    """
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



class CustomPermissions(BasePermission):
    def has_permission(self, request, view):
        if self._is_admin(request.user):
            return True
        return request.method in SAFE_METHODS or request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        if self._is_admin(request.user):
            return True
        return request.method in SAFE_METHODS or self._is_owner(request.user, obj)

    def _is_admin(self, user):
        return self._get_role_or_none(user) == 'admin'

    def _get_role_or_none(self, user):
        return getattr(user, 'role', None)

    def _is_owner(self, user, obj):
        return obj.author == user


