from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from user.forms import UserCreationForm
from user.models import CustomUser
from rest_framework import status
from verify_email.email_handler import send_verification_email
from django.http import HttpResponseRedirect
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
                user = CustomUser.objects.get(email=email)
                if user.check_password(password):
                    return user
            except CustomUser.DoesNotExist:
                pass
        return None


class Signup(APIView):
    def post(self, request):
        form = UserCreationForm(request.data)
        if form.is_valid():
            print(form)
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
     return render(request, 'registration/password_reset.html')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_email_sent')
   
    def form_valid(self, form):
        response = super().form_valid(form)
        self.success_message = "Your password has been successfully reset."
        return response
    
 
def password_reset_email_sent(request):
    return render(request, 'email_sent.html')   