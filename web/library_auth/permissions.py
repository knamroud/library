from rest_framework import permissions


class IsLibrarian(permissions.BasePermission):
    """
    Allows access only to Librarian users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Librarian').exists()


class IsLibrarianOrReadOnly(permissions.BasePermission):
    """
    Allows access only to Librarian users or authenticated users if the request is a read-only request.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in permissions.SAFE_METHODS or IsLibrarian().has_permission(request, view)
