from rest_framework import serializers
from movies.serializers import MovieSerializer
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        exclude = ["password"]
