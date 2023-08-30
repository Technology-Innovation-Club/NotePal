from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import os
from note.models import NoteFileembedding
from chat.models import NoteEmbedding


# class UploadTestCase(TestCase):
#     def setUp(self):
#         # Create a user
#         self.user = User.objects.create_user(
#             username="test@example.com",
#             email="test@example.com",
#             password="testpassword",
#         )

#     def test_successful_upload(self):
#         # Log in the user
#         self.client.login(username="test@example.com", password="testpassword")

#         # Create a test file
#         file_content = b'This is a test file content'
#         file = SimpleUploadedFile("test_file.pptx", file_content, content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")

#         # Send a POST request with the test file
#         response = self.client.post(reverse("api-1.0.0:file_upload"), {"file": file})

#         # Check if the upload was successful
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(NoteFileembedding.objects.count(), 1)
#         self.assertTrue(NoteEmbedding.objects.count() > 0)
#         self.assertTrue(response.json())

        

#     def tearDown(self):
#         # Log out the user
#         self.client.logout()
    
    # Test for uploading a successful file
    # Test for uploading a file without logging in
    # Test for uploading a file with a different file type
    # Test for uploading a file with the same name as an existing file
    # Test for uploading a file with a name that is too long
    # Test for uploading multiple files at once
    # Test for uploading a file is too short
    # Test for uploading nothing