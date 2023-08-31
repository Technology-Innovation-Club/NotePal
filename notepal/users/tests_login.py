from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User





class LoginTestCase(TestCase):
    def setUp(self):
        pass
    
    # login successful
    def test_successful_login(self):
        # Create a user
        User.objects.create_user(
            username= "invalid@example.com",
            email="test@example.com",
            password="testpassword",
        )

        # Send a POST request with valid login credentials
        login_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(reverse("api-1.0.0:tic_login"), login_data)
        self.assertEqual(response.status_code, 200)

    # missing fields - backend
    def test_invalid_login_missing_fields(self):
        login_data = {
            "email": "",
            "password": "",
        }
        response = self.client.post(reverse("api-1.0.0:tic_login"), login_data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(User.objects.count(), 0)
        
    # authentication error - backend
    def test_invalid_login(self):
        login_data = {
            "email": "invalid@example.com",
            "password": "invalidpassword",
        }
        response = self.client.post(reverse("api-1.0.0:tic_login"), login_data)
        self.assertEqual(response.status_code, 401)  # Unauthorized status
        self.assertEqual(response.json(), {'detail': "{'Authentication error': 'Wrong credentials'}"})
    
    # wrong password
    def test_incorrect_password(self):
        # Create a user with a known password
        User.objects.create_user(
            username= "invalid@example.com",
            email="test@example.com",
            password="testpassword",
        )

        # Send a POST request with correct email but incorrect password
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword",
        }
        response = self.client.post(reverse("api-1.0.0:tic_login"), login_data)
        self.assertEqual(response.status_code, 401)  # Unauthorized status
        self.assertEqual(response.json(), {'detail': "{'Authentication error': 'Wrong credentials'}"})
    
    # nonexistent user
    def test_nonexistent_user(self):
        # Send a POST request with an email that doesn't exist
        login_data = {
            "email": "nonexistent@example.com",
            "password": "somepassword",
        }
        response = self.client.post(reverse("api-1.0.0:tic_login"), login_data)
        self.assertEqual(response.status_code, 401)  # Unauthorized status
        self.assertEqual(response.json(), {'detail': "{'Authentication error': 'Wrong credentials'}"})
        
    # check user activity
    def test_inactive_user(self):
        # Create an inactive user
        User.objects.create(
            username= "invalid@example.com",
            email="inactive@example.com",
            password="testpassword",
            is_active=False,
        )

        # Send a POST request with the credentials of the inactive user
        login_data = {
            "email": "inactive@example.com",
            "password": "testpassword",
        }
        response = self.client.post(reverse("api-1.0.0:tic_login"), login_data)
        self.assertEqual(response.status_code, 401)  # Unauthorized status
        # self.assertEqual(response.json(), {'detail': "{'Authentication error': 'User is not active'}"})
    
