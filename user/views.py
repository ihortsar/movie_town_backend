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

# Create your views here.

"""Custom login view that inherits from ObtainAuthToken to handle user authentication
    and return an authentication token."""
class CustomLoginView(ObtainAuthToken):
    
    """ Handle POST requests to authenticate a user and provide an auth token.

        Args:
            request (Request): The HTTP request object containing email and password.

        Returns:
            Response: A response containing the auth token, user details, and user's videos."""

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if email is None or password is None:
            return Response(
                {"error": "Please provide both email and password"}, status=400
            )

        # Authenticate the user using email and password
        user = self.authenticate(email=email, password=password)
        # If user authentication fails, return an error response
        if not user:
            return Response({"error": "Invalid email or password"}, status=400)
        if not user.is_active:
            return Response({"error": "Confirm your Email"}, status=400)
        # Generate or retrieve the authentication token for the user
        token, created = Token.objects.get_or_create(user=user)
        users_videos = Movie.objects.filter(user=user)
        users_videos = MovieSerializer(users_videos, many=True).data
        # Return the authentication token along with user details
        return Response(
            {
                "token": token.key,
                "user": UserSerializer(user).data,
                "email": user.email,
                "users_videos": users_videos,
            }
        )
        

    """Authenticate a user based on email and password.
        Args:
            email (str): User's email address.
            password (str): User's password.

        Returns:
            User: Authenticated user object if successful, otherwise None."""
    def authenticate(self, email=None, password=None):
        # Use Django's authentication mechanism to authenticate the user using email and password
        if email and password:
            try:
                user = User.objects.get(email=email)
                print("Retrieved user:", user)
                if user.check_password(password):
                    print("Password matched")

                    return user
                else:
                    print("Password did not match")

            except User.DoesNotExist:
                pass
        return None


"""View for user registration. Handles creating a new user and sending a verification email."""
class SignUp(APIView):
    def post(self, request):
        """
        Handle POST requests to register a new user and send a verification email.

        Args:
            request (Request): The HTTP request object containing user data.

        Returns:
            Response: A response indicating the success or failure of user registration.
        """
        form = UserCreationForm(request.data["data"])
        if form.is_valid():
            form.save()
            send_verification_email(request, form)
            return Response(
                {
                    "message": "User created successfully. Check your email for verification."
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            print(form.errors)  # Debugging: Print form errors
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)



"""
    View for updating the profile of the currently authenticated user.
"""
class CurrentUser(APIView):
    """
        Handle PUT requests to update user details and change password.

        Args:
            request (Request): The HTTP request object containing updated user data.

        Returns:
            Response: A response indicating the success or failure of the update operation.
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


"""
    Middleware to redirect users to the frontend login page if they are not authenticated
    and trying to access verification endpoints.
"""
class FrontendLoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
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
        HttpResponse: Rendered password reset page.
    """
    return render(request, "registration/password_reset.html")


"""
    View for handling the password reset process, including rendering the password reset form
    and handling successful password reset submissions.
"""
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    
    template_name = "password_reset.html"
    email_template_name = "password_reset_email.html"
    success_url = reverse_lazy("password_reset_email_sent")

    def form_valid(self, form):
        """
        Handle a valid password reset form submission.

        Args:
            form (Form): The valid password reset form.

        Returns:
            HttpResponse: Redirects to the success URL with a success message.
        """
        response = super().form_valid(form)
        self.success_message = "Your password has been successfully reset."
        return response


def password_reset_email_sent(request):
    return render(request, "email_sent.html")


"""
    View for adding a movie to the user's selected movies list.
"""
class Movie_Select(APIView):
    """
        Handle POST requests to add a movie to the user's selected movies list.

        Args:
            request (Request): The HTTP request object containing movie data and user ID.
        Returns:
            Response: A response indicating success or failure of adding the movie.
        """
    def post(self, request):
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
