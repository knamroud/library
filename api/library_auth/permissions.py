from rest_framework import permissions

class IsLibrarian(permissions.BasePermission):
    """
    Allows access only to Librarian users.
    """
    def has_permission(self, request, view):
        return  request.user.is_authenticated and request.user.groups.filter(name='Librarian').exists()
