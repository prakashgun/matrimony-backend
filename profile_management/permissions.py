from rest_framework import permissions


class InterestDecisionAndDelete(permissions.BasePermission):
    """
    Object-level permission to only allow interest receivers to accept it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE' and \
                obj.from_profile.user == request.user:
            return True

        # Interest receiver should only accept it, no one else
        return obj.to_profile.user == request.user
