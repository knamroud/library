from django.contrib.auth.models import User, Group
from .models import Author, Book, Loan
from . import serializers
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.db.models import Q
from functools import reduce


class AuthorViewTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", password="testpassword")
        user.save()
        self.utoken = Token.objects.create(user=user)
        self.utoken.save()
        librarian = User.objects.create_user(
            username="librarian", password="librarian")
        librarian.groups.set([Group.objects.get(name="Librarian")])
        librarian.save()
        self.ltoken = Token.objects.create(user=librarian)
        self.ltoken.save()

    def test_author_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.utoken.key)
        author = Author.objects.create(
            first_name="test", last_name="test", birth="2020-01-01")
        author.save()
        response = self.client.get("/api/authors")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [serializers.AuthorSerializer(author).data], response.data["results"])

    def test_unauthorized_author_create(self):
        data = {"first_name": "test",
                "last_name": "test", "birth": "2020-01-01"}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.utoken.key)
        response = self.client.post(
            "/api/authors", data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Author.objects.filter(
            first_name=data["first_name"], last_name=["last_name"]).exists())

    def test_author_create(self):
        data = {"first_name": "test",
                "last_name": "test", "birth": "2020-01-01"}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.ltoken.key)
        response = self.client.post(
            "/api/authors", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Author.objects.filter(
            first_name=data["first_name"], last_name=data["last_name"]).exists())


class AuthorDetailViewTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", password="testpassword")
        user.save()
        self.utoken = Token.objects.create(user=user)
        self.utoken.save()
        librarian = User.objects.create_user(
            username="librarian", password="librarian")
        librarian.groups.set([Group.objects.get(name="Librarian")])
        librarian.save()
        self.ltoken = Token.objects.create(user=librarian)
        self.ltoken.save()
        self.author = Author.objects.create(
            first_name="test", last_name="test", birth="2020-01-01")
        self.author.save()

    def test_author_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.utoken.key)
        response = self.client.get(f"/api/authors/{self.author.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data, serializers.AuthorSerializer(self.author).data)

    def test_unauthorized_author_update(self):
        data = {"first_name": "test2",
                "last_name": "test2", "birth": "2020-03-01"}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.utoken.key)
        response = self.client.put(
            f"/api/authors/{self.author.id}", data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Author.objects.filter(
            first_name=data["first_name"], last_name=["last_name"]).exists())

    def test_author_update(self):
        data = {"first_name": "test2",
                "last_name": "test2", "birth": "2020-03-01"}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.ltoken.key)
        response = self.client.put(
            f"/api/authors/{self.author.id}", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Author.objects.filter(
            first_name=data["first_name"], last_name=data["last_name"]).exists())

    def test_unauthorized_author_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.utoken.key)
        response = self.client.delete(
            f"/api/authors/{self.author.id}")
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Author.objects.filter(
            first_name=self.author.first_name, last_name=self.author.last_name).exists())

    def test_author_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.ltoken.key)
        response = self.client.delete(
            f"/api/authors/{self.author.id}")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Author.objects.filter(
            first_name=self.author.first_name, last_name=self.author.last_name).exists())


class BookViewTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", password="testpassword")
        user.save()
        self.utoken = Token.objects.create(user=user)
        self.utoken.save()
        librarian = User.objects.create_user(
            username="librarian", password="librarian")
        librarian.groups.set([Group.objects.get(name="Librarian")])
        librarian.save()
        self.ltoken = Token.objects.create(user=librarian)
        self.ltoken.save()
        self.author = Author.objects.create(
            first_name="test", last_name="test", birth="2020-01-01")
        self.author.save()

    def test_book_list(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.utoken.key)
        book = Book.objects.create(
            title="test", isbn="test", year=2020)
        book.authors.set([self.author])
        book.save()
        response = self.client.get("/api/books")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [serializers.BookSerializer(book).data], response.data["results"])

    def test_unauthorized_book_create(self):
        data = {"title": "test",
                "authors": [1], "isbn": "test", "year": 2020}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.utoken.key)
        response = self.client.post(
            "/api/books", data)
        self.assertEqual(response.status_code, 403)
        q = reduce(lambda x, y: x & y, [
                   Q(authors__id=author_id) for author_id in data["authors"]])
        self.assertFalse(Book.objects.filter(
            title=data["title"]).filter(q).exists())

    def test_book_create(self):
        data = {"title": "test",
                "authors": [1], "isbn": "test", "year": 2020}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.ltoken.key)
        response = self.client.post(
            "/api/books", data)
        self.assertEqual(response.status_code, 201)
        q = reduce(lambda x, y: x & y, [
                   Q(authors__id=author_id) for author_id in data["authors"]])
        self.assertTrue(Book.objects.filter(
            title=data["title"]).filter(q).exists())


class BookDetailViewTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", password="testpassword")
        user.save()
        self.utoken = Token.objects.create(user=user)
        self.utoken.save()
        librarian = User.objects.create_user(
            username="librarian", password="librarian")
        librarian.groups.set([Group.objects.get(name="Librarian")])
        librarian.save()
        self.ltoken = Token.objects.create(user=librarian)
        self.ltoken.save()
        self.author = Author.objects.create(
            first_name="test", last_name="test", birth="2020-01-01")
        self.author.save()
        self.book = Book.objects.create(
            title="test", isbn="test", year=2020)
        self.book.authors.set([self.author])
        self.book.save()

    def test_book_retrieve(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.utoken.key)
        response = self.client.get(f"/api/books/{self.book.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data, serializers.BookSerializer(self.book).data)

    def test_unauthorized_book_update(self):
        data = {"title": "test2",
                "authors": [1], "isbn": "test2", "year": 2022}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.utoken.key)
        response = self.client.put(
            f"/api/books/{self.book.id}", data)
        self.assertEqual(response.status_code, 403)
        q = reduce(lambda x, y: x & y, [
                   Q(authors__id=author_id) for author_id in data["authors"]])
        self.assertFalse(Book.objects.filter(
            title=data["title"]).filter(q).exists())

    def test_book_update(self):
        data = {"title": "test2",
                "authors": [1], "isbn": "test2", "year": 2022}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.ltoken.key)
        response = self.client.put(
            f"/api/books/{self.book.id}", data)
        self.assertEqual(response.status_code, 200)
        q = reduce(lambda x, y: x & y, [
                   Q(authors__id=author_id) for author_id in data["authors"]])
        self.assertTrue(Book.objects.filter(
            title=data["title"]).filter(q).exists())

    def test_unauthorized_book_delete(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.utoken.key)
        response = self.client.delete(
            f"/api/books/{self.book.id}")
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Book.objects.filter(
            title=self.book.title).exists())

    def test_book_delete(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.ltoken.key)
        response = self.client.delete(
            f"/api/books/{self.book.id}")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Book.objects.filter(
            title=self.book.title).exists())


class LoanViewTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", password="testpassword")
        user.save()
        self.token = Token.objects.create(user=user)
        self.token.save()
        self.author = Author.objects.create(
            first_name="test", last_name="test", birth="2020-01-01")
        self.author.save()
        self.book = Book.objects.create(
            title="test", isbn="test", year=2020, availability=5)
        self.book.authors.set([self.author])
        self.book.save()
        self.loan = Loan.objects.create(
            book=self.book, borrower=user, date_due="2020-01-01")
        self.loan.save()

    def test_loan_list(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/loans")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [serializers.LoanSerializer(self.loan).data], response.data["results"])

    def test_loan_create(self):
        data = {"book": self.book.id}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(
            "/api/loans", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Loan.objects.filter(
            borrower=1, book=self.book.id).exists())


class LoanDetailViewTestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name="test", last_name="test", birth="2020-01-01")
        self.author.save()
        self.book = Book.objects.create(
            title="test", isbn="test", year=2020)
        self.book.authors.set([self.author])
        self.book.save()
        user = User.objects.create_user(
            username="testuser", password="testpassword")
        user.save()
        self.utoken = Token.objects.create(user=user)
        self.utoken.save()
        nuser = User.objects.create_user(
            username="nuser", password="nuser")
        self.ntoken = Token.objects.create(user=nuser)
        self.ntoken.save()
        librarian = User.objects.create_user(
            username="librarian", password="librarian")
        librarian.groups.set([Group.objects.get(name="Librarian")])
        librarian.save()
        self.ltoken = Token.objects.create(user=librarian)
        self.ltoken.save()
        self.loan = Loan.objects.create(
            book=self.book, borrower=user, date_due="2020-01-01")
        self.loan.save()

    def test_unauthorized_retrieve(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.ntoken.key)
        response = self.client.get(f"/api/loans/{self.loan.id}")
        self.assertEqual(response.status_code, 404)

    def test_loan_retrieve(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.utoken.key)
        response = self.client.get(f"/api/loans/{self.loan.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data, serializers.LoanSerializer(self.loan).data)

    def test_loan_unauthorized_update(self):
        data = {"date_due": "2020-02-01", "date_returned": "2020-01-01"}
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.utoken.key)
        response = self.client.put(
            f"/api/loans/{self.loan.id}", data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Loan.objects.filter(
            date_returned=data["date_returned"], date_due=data["date_due"]).exists())

    def test_loan_update(self):
        data = {"date_due": "2020-02-01", "date_returned": "2020-01-01"}
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.ltoken.key)
        response = self.client.put(
            f"/api/loans/{self.loan.id}", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Loan.objects.filter(
            date_returned=data["date_returned"], date_due=data["date_due"]).exists())
