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


class IsOwnInterestOrDisallow(permissions.BasePermission):
    """
    Object-level permission to see only sent or received interests
    """

    def has_object_permission(self, request, view, obj):
        # Interest receiver should only accept it, no one else
        return (obj.to_profile.user == request.user) or (
                    obj.to_profile.user == request.user)
