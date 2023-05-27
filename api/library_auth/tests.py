from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegisterViewTestCase(TestCase):
    def test_register(self):
        data = {
            "username": "testuser",
            "first_name": "test",
            "last_name": "user",
            "email": "test@test.com",
            "password": "testpassword",
            "cpassword": "testpassword"
        }
        response = self.client.post("/auth/register/", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username=data["username"]).exists())
    
class LoginViewTestCase(TestCase):
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
        response = self.client.post("/auth/login/", data)
        self.assertEqual(response.status_code, 202)
        token = response.data["token"]
        self.assertTrue(Token.objects.filter(key=token, user=self.user).exists())

class LogoutViewTestCase(TestCase):
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

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.post("/auth/logout/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Token.objects.filter(key=self.token).exists())

class MeViewTestCase(TestCase):
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
    
    def test_get_me(self):
        self.client.force_login(self.user)
        response = self.client.get("/auth/me/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["first_name"], self.user.first_name)
        self.assertEqual(response.data["last_name"], self.user.last_name)
        self.assertEqual(response.data["email"], self.user.email)
    
    def test_delete_me(self):
        self.client.force_login(self.user)
        response = self.client.delete("/auth/me/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=self.user.username).exists())
        self.assertFalse(Token.objects.filter(key=self.token).exists())
    
    def test_post_me(self):
        self.client.force_login(self.user)
        data = {
            "username": "testuser2",
            "first_name": "test2",
            "last_name": "user2",
            "email": "test@user2.com",
            "new_password": "testpassword2",
            "old_password": "testpassword"
        }
        response = self.client.post("/auth/me/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], data["username"])
        self.assertEqual(response.data["first_name"], data["first_name"])
        self.assertEqual(response.data["last_name"], data["last_name"])
        self.assertEqual(response.data["email"], data["email"])
        self.assertTrue(self.user.check_password(data["new_password"]))
