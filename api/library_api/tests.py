from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Author, Book, Loan
from . import serializers
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# write test cases for author view


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
        self.assertIn(
            serializers.AuthorSerializer(author).data, response.data["results"])

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
