from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CustomUser  

class CustomLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='test@example.com', password='testpassword')

    def test_login(self):
        url = reverse('login')  
        response = self.client.post(url, {'email': 'test@example.com', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_signup(self):
        url = reverse('signup') 
        data = {
            'data': {
                'email': 'test@example.com',
                'password1': 'testpassword',
                'password2': 'testpassword',
                'firstName': 'Test',
                'lastName': 'User',
                'birthday': '2000-01-01'
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
