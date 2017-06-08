from rest_framework import permissions


class BlackListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False
