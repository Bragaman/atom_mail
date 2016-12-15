
from finance.models import *


class IsSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        else:
            return False
