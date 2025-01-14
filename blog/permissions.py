from rest_framework.permissions import BasePermission
from .models import User

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and not User.objects.exists():
            # Allow unauthenticated access to create the first user
            return True
        # Otherwise, check if the user is authenticated
        return request.user and request.user.is_authenticated and request.user.role == 'Owner'

class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'Admin' or request.user.role == 'Owner'
        )

class IsMemberOrHigher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Member', 'Admin', 'Owner']
