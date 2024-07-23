from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer


class Video(APIView):
    
    def get(self, request, *args, **kwargs):
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
        movie_serializer = MovieSerializer(data=request.data)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return Response(movie_serializer.data, status=201)
        else:
            return Response(movie_serializer.errors, status=400)

   

    def delete(self, request, *args, **kwargs):
        movie_id = kwargs.get("movie_id")
        movie = get_object_or_404(Movie, pk=movie_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

