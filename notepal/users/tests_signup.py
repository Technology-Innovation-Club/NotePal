from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class SignupTestCase(TestCase):
    def setUp(self):
        pass
    
    # signup sucessful
    def test_successful_signup(self):
        signup_data = {
            "email": "john@example.com",
            "password": "securepassword",
            "repeat_password": "securepassword",
        }
        response = self.client.post(reverse("api-1.0.0:signup"), signup_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, "john@example.com")
        

    # missing fields - backend
    def test_invalid_signup_missing_fields(self):
        signup_data = {
            "email": "",
            "password": "",
            "repeat_password": "",
        }
        response = self.client.post(reverse("api-1.0.0:signup"), signup_data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'detail': "{'email': 'Email is required', 'password': 'Password is required', 'repeat_password': 'Repeat password is required'}"})
        self.assertEqual(User.objects.count(), 0)

    # password mismatch - backend
    def test_invalid_signup_password_mismatch(self):
        signup_data = {
            "email": "alice@example.com",
            "password": "password1",
            "repeat_password": "password2",  # Mismatched password
        }
        response = self.client.post(reverse("api-1.0.0:signup"), signup_data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'detail': "{'password': 'Passwords do not match'}"})
        self.assertEqual(User.objects.count(), 0)
        
    # invalid email - backend
    def test_invalid_signup_email(self):
        signup_data = {
            "email": "alice",  # Invalid email
            "password": "password1",
            "repeat_password": "password1",
        }
        response = self.client.post(reverse("api-1.0.0:signup"), signup_data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'detail': "{'email': 'Invalid email address'}"})
        self.assertEqual(User.objects.count(), 0)

    # email already exists - backend
    def test_unique_email_signup(self):
        existing_email = "existing@example.com"
        User.objects.create(email=existing_email)

        signup_data = {
            "email": existing_email,  # Use existing email
            "password": "securepassword",
            "repeat_password": "securepassword",
        }

        response = self.client.post(reverse("api-1.0.0:signup"), signup_data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'detail': "{'email': 'Email is already in use'}"})
        self.assertEqual(User.objects.count(), 1)

    # check that strong password is enforced
    def test_password_length(self):
        short_password_data = {
            "email": "short@example.com",
            "password": "shortpa",  # Password less than 8 characters
            "repeat_password": "shortpa",
        }
        response = self.client.post(reverse("api-1.0.0:signup"), short_password_data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'detail': "{'password': 'Password is too short. It must be at least 8 characters long'}"})
        self.assertEqual(User.objects.count(), 0)

        long_password_data = {
            "full_name": "Long Password",
            "email": "long@example.com",
            "password": "verylongpassword",  # Password more than 8 characters
            "repeat_password": "verylongpassword",
        }
        response = self.client.post(reverse("api-1.0.0:signup"), long_password_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, "long@example.com")


