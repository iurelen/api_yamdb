import sys

from rest_framework.permissions import BasePermission, SAFE_METHODS


class CustomPermissions(BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        print(self._is_admin(request.user), '_________')
        if self._is_admin(request.user):
            return True
        return request.method in SAFE_METHODS or request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        if self._is_admin(request.user):
            return True
        return request.method in SAFE_METHODS or self._is_owner(request.user, obj)

    def _is_admin(self, user):
        print(self._get_role_or_none(user))
        return self._get_role_or_none(user) == 'admin'

    def _get_role_or_none(self, user):
        return getattr(user, 'role', None)

    def _is_owner(self, user, obj):
        return obj.author == user

class TestPermissions(BasePermission):
    pass