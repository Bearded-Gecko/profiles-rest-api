from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS: #check if request is in the safe method, e.g., get
            return True

        return obj.id == request.user.id #otherwise, if using update or delete, or similar, we will return result if obj id is equal to request.user.id

class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""
    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id #if object being modified has user profile id same as request.user id, then true
