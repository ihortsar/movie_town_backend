from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from user.forms import User, UserCreationForm
from rest_framework import status
from verify_email.email_handler import send_verification_email
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

# Create your views here.


class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Get the email and password from the request data
        email = request.data.get("email")
        password = request.data.get("password")

        # Validate the email and password
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

        # Return the authentication token along with user details
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})

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


class SignUp(APIView):
    def post(self, request):
        form = UserCreationForm(request.data)
        if form.is_valid():
            form.save()  # Save the user directly using the form
            send_verification_email(request, form)
            return Response(
                {
                    "message": "User created successfully. Check your email for verification."
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUser(APIView):
    def post(self, request):
        try:
            # Attempt to retrieve the user based on the provided user_id
            current_user = User.objects.get(pk=request.data.get("user_id"))
            return JsonResponse(
                {
                    "user": [
                        {"email": current_user.email},
                        {"first_name": current_user.first_name},
                        {"last_name": current_user.last_name},
                        {"adress": current_user.address},
                    ]
                },
                status=200,
            )
        except User.DoesNotExist:
            # If user with the provided user_id does not exist, return an error response
            return JsonResponse({"error": "User not found"}, status=404)

    def put(self, request):
        # Check if the user exists
        try:
            current_user = User.objects.get(pk=request.data.get("id"))
        except User.DoesNotExist:
            # If user with the provided primary key does not exist, return a 404 response
            return JsonResponse({"error": "User not found"}, status=404)

        # If the user exists, save the user's data and return a success response
        current_user.save()
        return JsonResponse({"message": "User data updated successfully"})


class FrontendLoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if "/verification/user/verify-email/" in request.path:
            # Redirect to the frontend login page if the user is not authenticated
            if not request.user.is_authenticated:
                return HttpResponseRedirect("http://localhost:4200")

        return response


def password_reset(request):
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
        movie_data = request.data.get('movie')  # Access movie data from the request
        user_id = request.data.get('user_id')  
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Add the movie to the user's selected_movies list
        user.selected_movies.append(movie_data)

        # Save the changes to the user object
        user.save()
        return Response(
            {"message": "Movie added to selected movies"},
            status=status.HTTP_201_CREATED,
        )
