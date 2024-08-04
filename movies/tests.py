from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from user.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile


class MovieTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        
        self.user = CustomUser.objects.create_user(
            email="testuser@test.com", password="testpassword"
        )

        self.video_file = SimpleUploadedFile(
            name="test_video.mp4", content=b"fake content", content_type="video/mp4"
        )

        self.movie = {
            "title": "Test Movie",
            "description": "Test Description",
            "video_file": self.video_file,
            "user": self.user.id,
        }

        self.url = reverse("video")
        self.delete_url = reverse("video")

    def test_create_movie(self):
        response = self.client.post(
            self.url,
            {
                "title": self.movie["title"],
                "description": self.movie["description"],
                "video_file": self.movie["video_file"],
                "user": self.movie["user"],
            },
            format="multipart",
        )
        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Test Movie")
        self.assertEqual(response.data["user"], self.user.id)
