from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.utils.decorators import method_decorator


CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class Video(APIView):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        """
        Retrieve the list of movies based on their access settings.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments, including `user_id` for private videos.

        Returns:
            Response: A `Response` object containing the list of movies in JSON format or an error message.
        """
        user_id = kwargs.get("user_id")
        try:
            public_videos = Movie.objects.filter(access="public")
            if user_id:
                private_videos = Movie.objects.filter(user=user_id, access="private")
            else:
                private_videos = Movie.objects.none()

            videos = public_videos | private_videos

            if not videos.exists():
                return Response([], status=status.HTTP_200_OK)

            serializer = MovieSerializer(videos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, *args, **kwargs):
        """
        Create a new movie entry.

        Args:
            request: The HTTP request object containing movie data.

        Returns:
            Response: A `Response` object containing the serialized movie data or validation errors.
        """
        movie_serializer = MovieSerializer(data=request.data)
        if movie_serializer.is_valid():
            movie_serializer.validated_data["access"] = request.data.get(
                "access", "private"
            )
            movie_serializer.save()
            return Response(movie_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Delete a specific movie entry.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments, including `movie_id`.

        Returns:
            Response: An empty `Response` with a 204 status code if the deletion is successful.
        """
        movie_id = kwargs.get("movie_id")
        movie = get_object_or_404(Movie, pk=movie_id)

        if movie.access == "private" and movie.user != request.user:
            return Response(
                {"error": "Not authorized to delete this movie."},
                status=status.HTTP_403_FORBIDDEN,
            )

        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
