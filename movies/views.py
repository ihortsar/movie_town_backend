from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Movie
from .serializers import MovieSerializer


class Video(APIView):
    """
    API view for handling video-related operations, including retrieving, creating, and deleting movies.
    
    Authentication and permissions:
    - `TokenAuthentication` is required to access this view.
    - `IsAuthenticated` permission ensures that only authenticated users can interact with this view.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """
        Retrieve the list of movies associated with a specific user.
        
        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments, including `user_id`.

        Returns:
            Response: A `Response` object containing the list of movies in JSON format or an error message.
        """
        user_id = kwargs.get("user_id")
        try:
            users_videos = Movie.objects.filter(user=user_id)
            
            if not users_videos.exists():
                return Response([], status=status.HTTP_200_OK)
           
            serializer = MovieSerializer(users_videos, many=True)
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
            movie_serializer.save()
            return Response(movie_serializer.data, status=201)
        else:
            return Response(movie_serializer.errors, status=400)

   

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
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

