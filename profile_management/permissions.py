from rest_framework import permissions


class IsInterestReceiverOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow interest receivers to accept it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Interest receiver should only accept it, no one else
        return obj.to_profile.user == request.user


class IsOwnShortlistOrDisallow(permissions.BasePermission):
    """
    Object-level permission to see only own shortlists
    """

    def has_object_permission(self, request, view, obj):
        return obj.from_profile.user == request.user
