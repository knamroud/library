from rest_framework import generics
from library_auth.permissions import IsLibrarian
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Author, Book, Loan
from . import serializers


class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly | IsLibrarian]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly | IsLibrarian]


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly | IsLibrarian]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly | IsLibrarian]


class LoanListCreateView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = serializers.LoanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly | IsLibrarian]

    def get_queryset(self):
        return Loan.objects.filter(borrower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)
