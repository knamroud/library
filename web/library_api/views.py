from datetime import timedelta, date
from rest_framework import generics
from library_auth.permissions import IsLibrarian, IsLibrarianOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .models import Author, Book, Loan
from rest_framework.response import Response
from . import serializers
from rest_framework.serializers import ValidationError


class AuthorView(generics.ListCreateAPIView):
    queryset = Author.objects.all().order_by("last_name", "first_name")
    serializer_class = serializers.AuthorSerializer
    permission_classes = [IsLibrarianOrReadOnly]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    permission_classes = [IsLibrarianOrReadOnly]


class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by("title", "year")
    serializer_class = serializers.BookSerializer
    permission_classes = [IsLibrarianOrReadOnly]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = [IsLibrarianOrReadOnly]


class LoanView(generics.ListCreateAPIView):
    queryset = Loan.objects.all().order_by("date_due")
    serializer_class = serializers.LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(borrower=self.request.user).order_by("date_due", "date_returned")

    def perform_create(self, serializer):
        if serializer.validated_data["book"].availability > 0:
            serializer.save(borrower=self.request.user,
                            date_due=date.today() + timedelta(days=14))
            b = Book(id=serializer.validated_data["book"].id)
            b.availability -= 1
        else:
            raise ValidationError(
                {"book": "This book is not available"})


class LoanDetailView(generics.RetrieveUpdateAPIView):
    queryset = Loan.objects.all()
    serializer_class = serializers.LoanSerializer
    permission_classes = [IsLibrarianOrReadOnly]

    def get_queryset(self):
        return Loan.objects.filter(borrower=self.request.user) if not IsLibrarian().has_permission(self.request, self) else Loan.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        errors = dict()
        errors.update({"date_returned": "This field is required"}
                      if "date_returned" not in request.data else {})
        errors.update({"date_due": "This field is required"}
                      if "date_due" not in request.data else {})
        if errors:
            raise serializers.ValidationError(errors)
        data = {
            "date_returned": request.data["date_returned"], "date_due": request.data["date_due"]}
        serializer = self.get_serializer(
            instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        instance = self.get_object()
        if serializer.validated_data["date_returned"] > serializer.validated_data["date_due"]:
            serializer.save(fine=instance.book.price * 1.1)
        else:
            serializer.save()
        instance.book.availability += 1
        instance.book.save()
