from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class LogoutTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpassword",
        )

    def test_successful_logout(self):
        # Log in the user
        self.client.login(email="test@example.com", password="testpassword")

        # Send a GET request to log the user out
        response = self.client.get(reverse("api-1.0.0:tic_logout"))
        self.assertEqual(response.status_code, 200)  # Redirect status

        # Check that the user is logged out
        self.assertFalse(response.wsgi_request.user.is_authenticated)
