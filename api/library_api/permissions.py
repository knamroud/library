from rest_framework.permissions import BasePermission, IsAuthenticated


class HasLoanPermission(BasePermission):
    """
    Is the borrower of the loan
    """

    def has_object_permission(self, request, view, obj):
        return IsAuthenticated and obj.borrower == request.user
