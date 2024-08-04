from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie
from movies.serializers import MovieSerializer
from .serializers import UserSerializer
from user.forms import User, UserCreationForm
from rest_framework import status
from verify_email.email_handler import send_verification_email
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.urls import reverse



def authenticate_user(email, password):
    """
    Authenticate a user based on their email and password.
    
    Args:
        email (str): The email address of the user.
        password (str): The password of the user.
    
    Returns:
        User: The authenticated user object if credentials are valid, None otherwise.
    """
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None


def handle_login(email, password):
    """
    Handle user login, authenticate user, and return necessary details.
    
    Args:
        email (str): The email address of the user.
        password (str): The password of the user.
    
    Returns:
        tuple: A dictionary containing the token, user data, email, and user’s movies, and a status code.
    """
    user = authenticate_user(email, password)
    if not user:
        return {"error": "Invalid email or password"}, 400
    if not user.is_active:
        return {"error": "Confirm your Email"}, 400

    token, created = Token.objects.get_or_create(user=user)

    users_videos = Movie.objects.filter(user=user)
    users_videos = MovieSerializer(users_videos, many=True).data

    return {
        "token": token.key,
        "user": UserSerializer(user).data,
        "email": user.email,
        "users_videos": users_videos,
    }, 200


class CustomLoginView(APIView):
    """
        Handle POST requests for user login.
        
        Args:
            request (Request): The HTTP request object.
        
        Returns:
            Response: The response object containing the result of the login attempt.
        """
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if email is None or password is None:
            return Response(
                {"error": "Please provide both email and password"}, status=status.HTTP_400_BAD_REQUEST
            )

        result, status_code = handle_login(email, password)
        return Response(result, status=status_code)


class SignUp(APIView):
    """
        Handle POST requests for user registration.
        
        Args:
            request (Request): The HTTP request object containing user data.
        
        Returns:
            Response: The response object containing the result of the registration attempt.
        """
    def post(self, request):
        form = UserCreationForm(request.data["data"])
        if form.is_valid():
            form.save()
            send_verification_email(request, form)
            return Response({"message": "User created successfully. Check your email for verification."}, status=status.HTTP_201_CREATED)
        else:
            print(form.errors)  # Debugging: Print form errors
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUser(APIView):
    """
        Handle PUT requests to update user details.
        
        Args:
            request (Request): The HTTP request object containing user data.
        
        Returns:
            JsonResponse: The response object with the updated user data or error message.
        """
    def put(self, request):
        try:
            current_user = User.objects.get(pk=request.data.get("id"))
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        for key, value in request.data.items():
            setattr(current_user, key, value)
        old_password = request.data.get("old_password")
        if old_password and not check_password(old_password, current_user.password):
            return JsonResponse({"error": "Old password is incorrect"}, status=400)
        new_password = request.data.get("new_password")
        if new_password:
            current_user.password = make_password(new_password)
        current_user.save()

        return JsonResponse(data=UserSerializer(current_user).data, status=200)


class FrontendLoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request and redirect if necessary.
        
        Args:
            request (Request): The HTTP request object.
        
        Returns:
            HttpResponse or Response: The response object, possibly redirected.
        """
        response = self.get_response(request)

        if "/verification/user/verify-email/" in request.path:
            # Redirect to the frontend login page if the user is not authenticated
            if not request.user.is_authenticated:
                # Define the frontend URL to redirect to
                frontend_login_url = "https://movies-town.ihor-tsarkov.com"
                return HttpResponseRedirect(frontend_login_url)

        return response


def password_reset(request):
    """
    Render the password reset page.
    
    Args:
        request (Request): The HTTP request object.
    
    Returns:
        HttpResponse: The rendered password reset page.
    """
    return render(request, "registration/password_reset.html")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    
    template_name = "password_reset.html"
    email_template_name = "password_reset_email.html"
    success_url = reverse_lazy("password_reset_email_sent")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.success_message = "Your password has been successfully reset."
        return response


def password_reset_email_sent(request):
    return render(request, "email_sent.html")


class Movie_Select(APIView):
    def post(self, request):
        """
        Handle POST requests to add a movie to the user's selected movies.
        
        Args:
            request (Request): The HTTP request object containing movie and user data.
        
        Returns:
            Response: The response object indicating the result of the movie selection.
        """
        movie_data = request.data.get("movie")  # Access movie data from the request
        user_id = request.data.get("user_id")
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        user.selected_movies.append(movie_data)
        user.save()
        return Response(
            {"message": "Movie added to selected movies"},
            status=status.HTTP_201_CREATED,
        )