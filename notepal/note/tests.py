from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import os
from note.models import NoteFileembedding
from chat.models import NoteEmbedding


class UploadTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpassword",
        )

        # Read the test file content
        test_file_path = r"C:\Users\ziont\Downloads\check_colab.pdf"
        with open(test_file_path, "rb") as file:
            self.test_file_content = file.read()

        test_file_path2 = r"C:\Users\ziont\Downloads\check_colab.docx"
        with open(test_file_path2, "rb") as file:
            self.test_file_content2 = file.read()

        test_file_path3 = r"C:\Users\ziont\Downloads\check_colab.pptx"
        with open(test_file_path3, "rb") as file:
            self.test_file_content3 = file.read()

    # Test for uploading a successful PDF file
    def test_successful_upload_pdf(self):
        # Log in the user
        self.client.login(username="test@example.com", password="testpassword")

        # Create a test PDF file
        file = SimpleUploadedFile(
            "test_file.pdf", self.test_file_content, content_type="application/pdf"
        )

        # Send a POST request with the test file
        response = self.client.post(reverse("api-1.0.0:file_upload"), {"file": file})

        # Check if the upload was successful
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NoteFileembedding.objects.count(), 1)
        self.assertTrue(NoteEmbedding.objects.count() > 0)
        self.assertTrue(response.json())

    # Test for uploading a successful DOCX file
    def test_successful_upload_docx(self):
        # Log in the user
        self.client.login(username="test@example.com", password="testpassword")

        # Create a test DOCX file
        file = SimpleUploadedFile(
            "test_file.docx",
            self.test_file_content2,
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

        # Send a POST request with the test file
        response = self.client.post(reverse("api-1.0.0:file_upload"), {"file": file})

        # Check if the upload was successful
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NoteFileembedding.objects.count(), 1)
        self.assertTrue(NoteEmbedding.objects.count() > 0)
        self.assertTrue(response.json())

    # Test for uploading a successful PPTX file
    def test_successful_upload_pptx(self):
        # Log in the user
        self.client.login(username="test@example.com", password="testpassword")

        # Create a test PPTX file
        file = SimpleUploadedFile(
            "test_file.pptx",
            self.test_file_content3,
            content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )

        # Send a POST request with the test file
        response = self.client.post(reverse("api-1.0.0:file_upload"), {"file": file})

        # Check if the upload was successful
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NoteFileembedding.objects.count(), 1)
        self.assertTrue(NoteEmbedding.objects.count() > 0)
        self.assertTrue(response.json())

    # Test for uploading a file without logging in
    def test_upload_without_login(self):
        # Create a test file
        file = SimpleUploadedFile(
            "test_file.pdf", self.test_file_content, content_type="application/pdf"
        )

        # Send a POST request with the test file without logging in
        response = self.client.post(reverse("api-1.0.0:file_upload"), {"file": file})

        # Check if the response status code is 401 (Unauthorized)
        self.assertEqual(response.status_code, 401)

    # Test for uploading a file with a different file type
    def test_upload_wrong_file_type(self):
        # Log in the user
        self.client.login(username="test@example.com", password="testpassword")

        # Create a test file with a different content type (e.g., image/jpeg)
        file = SimpleUploadedFile(
            "test_file.jpg", self.test_file_content, content_type="image/jpeg"
        )

        # Send a POST request with the test file
        response = self.client.post(reverse("api-1.0.0:file_upload"), {"file": file})

        # Check if the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "detail": "{'File error': 'Invalid file type. Only pptx, docx, and pdf files are allowed.'}"
            },
        )

    # Test for uploading a file with the same name as an existing file
    def test_upload_existing_file_name(self):
        # Log in the user
        self.client.login(username="test@example.com", password="testpassword")

        # Create a test file
        file = SimpleUploadedFile(
            "test_file.pdf", self.test_file_content, content_type="application/pdf"
        )

        # Send a POST request with the test file
        response = self.client.post(reverse("api-1.0.0:file_upload"), {"file": file})

        # Check if the response status code is 200 (Success)
        self.assertEqual(response.status_code, 200)

        # Now try uploading a file with the same name
        duplicate_response = self.client.post(
            reverse("api-1.0.0:file_upload"), {"file": file}
        )

        # Check if the response status code is 409 (Conflict)
        self.assertEqual(duplicate_response.status_code, 409)
        self.assertEqual(
            duplicate_response.json(),
            {"detail": "{'File error': 'File with the same name already exists.'}"},
        )

    def tearDown(self):
        # Log out the user
        self.client.logout()


# POSSIBLE ADDITION
# Test for uploading a file with a name that is too long
