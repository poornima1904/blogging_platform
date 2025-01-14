from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import User

class CreateUserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and not User.objects.exists():
            # Allow unauthenticated access to create the first user
            return True
        # Otherwise, check if the user is authenticated
        return request.user and request.user.is_authenticated and request.user.role == 'Owner'

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Owner'

class CommentPermissionClass(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow owners and admins to create, edit, and delete articles.
    Members can only view articles.
    """

    def has_permission(self, request, view):
        # Allow all users to view articles (GET requests)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only owners and admins can create, update, or delete articles
        if request.user.role in ['Owner', 'Admin']:
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        # Allow owners and admins to edit or delete their articles
        if request.method in permissions.SAFE_METHODS:  # View (GET)
            return True
        
        if request.user.role in ['Owner', 'Admin']:
            return True

        # Members can only view (GET) the article
        return False

