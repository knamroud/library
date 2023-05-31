from rest_framework import serializers
from library_auth.serializers import UserSerializer
from .models import Author, Book, Loan
from django.utils.html import escape


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            if type(value) is str:
                data[key] = escape(value)
        return data


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), many=True, write_only=True)
    authors_details = serializers.SerializerMethodField(
        source="get_authors_details")

    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            if type(value) is str:
                data[key] = escape(value)
        return data

    def get_authors_details(self, obj):
        return AuthorSerializer(obj.authors.all(), many=True).data


class LoanSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), write_only=True)
    book_details = serializers.SerializerMethodField(source="get_book_details")
    borrower = UserSerializer(required=False)
    date_due = serializers.DateField(required=False)

    class Meta:
        model = Loan
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            if type(value) is str:
                data[key] = escape(value)
        return data

    def get_book_details(self, obj):
        return BookSerializer(obj.book).data
