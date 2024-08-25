import os
import subprocess
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from user.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile

class MovieTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Creates a test user
        self.user = CustomUser.objects.create_user(
            email="testuser@test.com", password="testpassword"
        )

        # Creates a small MP4 file using FFmpeg
        video_path = os.path.join(os.path.dirname(__file__), 'test_video.mp4')
        self.create_test_video(video_path)

        # Reads the video file into memory
        with open(video_path, 'rb') as video_file:
            self.video_file = SimpleUploadedFile(
                name="test_video.mp4", content=video_file.read(), content_type="video/mp4"
            )

        self.movie = {
            "title": "Test Movie",
            "description": "Test Description",
            "video_file": self.video_file,
            "user": self.user.id,
        }

        self.url = reverse("video")

    def create_test_video(self, path):
        """
        Creates a small MP4 video file using FFmpeg.
        """
        cmd = (
            f"ffmpeg -y -f lavfi -i color=c=black:s=640x480:d=1 "
            f"-f lavfi -i anullsrc=r=44100:cl=stereo "
            f"-shortest {path}"
        )
        subprocess.run(cmd, shell=True, check=True)

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

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Test Movie")
        self.assertEqual(response.data["user"], self.user.id)

    def tearDown(self):
        # Cleans up the created video file after the test
        video_path = os.path.join(os.path.dirname(__file__), 'test_video.mp4')
        if os.path.exists(video_path):
            os.remove(video_path)
