from django.contrib.auth.models import User
from rest_framework import permissions

class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Librarian').exists()
