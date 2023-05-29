from rest_framework import generics
from library_auth.permissions import IsLibrarian, IsLibrarianOrReadOnly
from rest_framework.response import Response
from .models import Author, Book, Loan
from . import serializers


class AuthorView(generics.ListCreateAPIView):
    queryset = Author.objects.all().order_by("last_name", "first_name")
    serializer_class = serializers.AuthorSerializer
    permission_classes = [IsLibrarianOrReadOnly]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    permission_classes = [IsLibrarianOrReadOnly]


class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by("title", "author", "year")
    serializer_class = serializers.BookSerializer
    permission_classes = [IsLibrarianOrReadOnly]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = [IsLibrarianOrReadOnly]


class LoanView(generics.ListCreateAPIView):
    queryset = Loan.objects.all().order_by("date_due")
    serializer_class = serializers.LoanSerializer
    permission_classes = [IsLibrarianOrReadOnly]

    def get_queryset(self):
        return Loan.objects.filter(borrower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)


class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = serializers.LoanSerializer
    permission_classes = [IsLibrarianOrReadOnly]

    def get_queryset(self):
        return Loan.objects.filter(borrower=self.request.user) if not IsLibrarian().has_permission(self.request, self) else Loan.objects.all()
