from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class UserAuthenticationTests(APITestCase):
    """Tests for user authentication"""

    def setUp(self):
        """Register test user"""
        user = User()
        user.username = 'testuser'
        user.email = 'test@email.com'
        user.password = 'pass1234'
        user.save()

    def test_access_without_token(self):
        """Test access to resources without token"""
        response = self.client.get('/bucketlists/')
        self.assertEqual(
            response.data, {"detail":
                            "Authentication credentials were not provided."})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_with_invalid_token(self):
        """Test accesss to resources with invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid')
        response = self.client.get('/bucketlists/')
        self.assertEqual(
            response.data, {"detail":
                            "Invalid token."})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_without_username_and_password_fields(self):
        """Test login without setting username and password"""
        response = self.client.post('/auth/login/')
        self.assertEqual(response.data, {"non_field_errors": [
                         "Unable to login with provided credentials."]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_blank_username_and_password(self):
        """Test login with  blank username and password fields"""
        data = {"username": "", "password": ""}
        response = self.client.post('/auth/login/', data=data)
        self.assertEqual(response.data, {"password": [
                         "This field may not be blank."],
            "username": ["This field may not be blank."]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_creadentials(self):
        """Test login with wrong username password combination"""
        data = {"username": "wrong", "password": "wrong"}
        response = self.client.post("/auth/login/", data=data)
        self.assertEqual(response.data, {"non_field_errors": [
                         "Unable to login with provided credentials."]})

    def test_registration_without_username_and_password_fields(self):
        """Test registration without any data"""
        response = self.client.post('/auth/register/')
        self.assertEqual(response.data, {"username": [
                         "This field is required."], "password":
            ["This field is required."]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_blank_username_and_password_fields(self):
        """Test registration with blank username and passwords"""
        data = {"username": "", "password": ""}
        response = self.client.post('/auth/register/', data=data)
        self.assertEqual(response.data, {"password": [
                         "This field may not be blank."], "username":
            ["This field may not be blank."]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_existing_username(self):
        """Test registration with username that exists"""
        response = self.client.post('/auth/register/',
                                    {'username': 'testuser',
                                     'password': 'testpass',
                                     'email': 'test@email.com'
                                     },
                                    format='json')
        self.assertEqual(response.data, {"username": [
                         "A user with that username already exists."]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
