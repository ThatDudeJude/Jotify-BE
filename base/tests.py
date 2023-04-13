from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

# Create your tests here.


class TestCustomUser(TestCase):
    def test_create_user(self):
        CustomUser = get_user_model()
        user = CustomUser.objects.create_user(
            email="user@example.com", name="userexample", password="1234567890"
        )
        user.save()
        self.assertEqual(CustomUser.objects.count(), 1)
        check_user = CustomUser.objects.get(email="user@example.com")
        self.assertEqual(check_user.name, "userexample")
        self.assertTrue(check_user.is_active)
        self.assertFalse(check_user.is_staff)
        self.assertFalse(check_user.is_superuser)

        try:
            self.assertIsNone(check_user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user()
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user(email="")
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email="", password="12343423", name="testfakeuser"
            )

    def test_create_superuser(self):
        CustomUser = get_user_model()
        superuser = CustomUser.objects.create_superuser(
            email="superuser@example.com", name="su", password="123456789"
        )
        self.assertEqual(superuser.email, "superuser@example.com")
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

        try:
            self.assertIsNone(superuser.username)
        except AttributeError:
            pass

        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                email="su@example.com",
                name="superuser",
                password="1324354343",
                is_staff=False,
            )


class TestAuthenticationAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.testuser = get_user_model().objects.create_user(
            name="testapiuser", email="testapiuser@example.com", password="123456789"
        )
        cls.testuser.save()

    def test_create_account(self):

        response = self.client.post(
            reverse("custom_signup"),
            {
                "name": "testusersignup",
                "email": "testsignup@example.com",
                "password": "1234546567",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertEqual(
            get_user_model().objects.all()[1].email, "testsignup@example.com"
        )

    def test_user_login(self):
        response = self.client.post(
            reverse("custom_login"),
            {
                "email": self.testuser.email,
                "password": "123456789",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json()["token"], Token.objects.get(user=self.testuser).key
        )
