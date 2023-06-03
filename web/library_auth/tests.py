from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token


class RegisterViewTestCase(APITestCase):
    def test_register(self):
        data = {
            "username": "testuser",
            "first_name": "test",
            "last_name": "user",
            "email": "test@test.com",
            "password": "testpassword",
            "cpassword": "testpassword"
        }
        response = self.client.post("/api/auth/register", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(
            username=data["username"]).exists())


class LoginViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            first_name="test",
            last_name="user",
            email="test@test.com",
            password="testpassword"
        )
        self.user.save()

    def test_login(self):
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post("/api/auth/login", data)
        self.assertEqual(response.status_code, 202)
        token = response.data["token"]
        self.assertTrue(Token.objects.filter(
            key=token, user=self.user).exists())


class LogoutViewTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser",
            first_name="test",
            last_name="user",
            email="test@user.com",
            password="testpassword"
        )
        user.save()
        self.token = Token.objects.create(user=user)
        self.token.save()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_logout(self):
        response = self.client.post("/api/auth/logout")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Token.objects.filter(key=self.token).exists())


class MeViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            first_name="test",
            last_name="user",
            email="test@user.com",
            password="testpassword"
        )
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_me(self):
        response = self.client.get("/api/auth/me")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["first_name"], self.user.first_name)
        self.assertEqual(response.data["last_name"], self.user.last_name)
        self.assertEqual(response.data["email"], self.user.email)

    def test_post_me(self):
        data = {
            "username": "testuser2",
            "first_name": "test2",
            "last_name": "user2",
            "email": "test@user2.com",
            "new_password": "testpassword2",
            "password": "testpassword"
        }
        response = self.client.post("/api/auth/me", data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.username, data["username"])
        self.assertEqual(self.user.first_name, data["first_name"])
        self.assertEqual(self.user.last_name, data["last_name"])
        self.assertEqual(self.user.email, data["email"])
        self.assertTrue(self.user.check_password(data["new_password"]))

    def test_delete_me(self):
        response = self.client.delete("/api/auth/me")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(
            username=self.user.username).exists())
        self.assertFalse(Token.objects.filter(key=self.token).exists())


class IsLibrarianTestCase(APITestCase):
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

    def test_is_librarian(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.ltoken.key)
        response = self.client.get("/api/auth/me")
        self.assertTrue(response.data["is_librarian"])

    def test_is_not_librarian(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.utoken.key)
        response = self.client.get("/api/auth/me")
        self.assertFalse(response.data["is_librarian"])
