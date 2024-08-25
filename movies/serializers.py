from rest_framework import serializers

from .models import Movie
from django.conf import settings
import os


class MovieSerializer(serializers.ModelSerializer):
    video_480p_url = serializers.SerializerMethodField()
    video_720p_url = serializers.SerializerMethodField()
    video_1080p_url = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "__all__"

    def get_video_480p_url(self, obj):
        return self.get_video_resolution_url(obj, "480p")

    def get_video_720p_url(self, obj):
        return self.get_video_resolution_url(obj, "720p")

    def get_video_1080p_url(self, obj):
        return self.get_video_resolution_url(obj, "1080p")

    def get_video_resolution_url(self, obj, resolution):
        if obj.video_file:
            video_path = obj.video_file.path
            base_name, ext = os.path.splitext(video_path)
            resolution_video_path = f"{base_name}_{resolution}{ext}"

            if os.path.exists(resolution_video_path):
                return settings.MEDIA_URL + os.path.relpath(
                    resolution_video_path, settings.MEDIA_ROOT
                )

        return None
