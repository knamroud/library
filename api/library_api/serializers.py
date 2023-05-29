from rest_framework.serializers import ModelSerializer
from library_auth.serializers import UserSerializer
from .models import Author, Book, Loan


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = '__all__'


class LoanSerializer(ModelSerializer):
    book = BookSerializer()
    borrower = UserSerializer()

    class Meta:
        model = Loan
        fields = '__all__'
