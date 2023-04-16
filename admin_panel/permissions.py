from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    """
    Allows access only to super admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff and request.user.is_superuser)
