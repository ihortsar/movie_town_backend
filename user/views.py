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
    """Authenticate user using email and password."""
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None


def handle_login(email, password):
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
    """Function-based view for user login."""
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
        response = self.get_response(request)

        if "/verification/user/verify-email/" in request.path:
            # Redirect to the frontend login page if the user is not authenticated
            if not request.user.is_authenticated:
                login_url = reverse('login')
                return HttpResponseRedirect(login_url)

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
