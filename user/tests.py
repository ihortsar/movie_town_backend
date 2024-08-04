import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime

User = get_user_model()


class CustomUserModelTests(TestCase):
    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "securepassword"
        User.objects.all().delete()  # Clean up existing users

    def test_user_manager_create_superuser(self):
        superuser = User.objects.create_superuser(
            email=self.email,
            password=self.password,
            first_name="John",
            last_name="Doe",
            birth_date="1990-01-01",
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.signup_url = reverse("signup")  # Ensure this is the correct URL name

    def test_signup_success(self):
        form_data = {
            "data": {  # Nest the form data under "data"
                "email": "testuser@example.com",
                "firstName": "John",  # Ensure these match the field names in the form
                "lastName": "Doe",
                "birthday": "1990-01-01",
                "password1": "securepassword",
                "password2": "securepassword",
            }
        }
        response = self.client.post(self.signup_url, form_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())


class UserUpdateTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            first_name="John",
            last_name="Doe",
            birth_date="1990-01-01",
            password="securepassword",
        )
        self.update_url = reverse(
            "current_user"
        )  # Ensure this matches your URL pattern

    def test_update_user_success(self):
        data = {
            "id": self.user.id,
            "first_name": "Jane",
            "last_name": "Doe",
            "birth_date": "1991-01-01",
            "old_password": "securepassword",
            "new_password": "newsecurepassword",
        }
        response = self.client.put(self.update_url, data, format="json")
        self.assertEqual(response.status_code, 200)

        # Check that the user details have been updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Jane")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(
            self.user.birth_date, datetime.strptime("1991-01-01", "%Y-%m-%d").date()
        )
        self.assertTrue(self.user.check_password("newsecurepassword"))


class UserManagerTests(TestCase):
    def setUpDelete(self):
        User.objects.all().delete()

    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "securepassword"
        self.user_model = get_user_model()

    def test_create_superuser(self):
        superuser = self.user_model.objects.create_superuser(
            email=self.email, password=self.password
        )
        self.assertTrue(superuser.is_superuser)
