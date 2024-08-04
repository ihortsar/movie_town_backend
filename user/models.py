from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


"""
    Custom manager for the CustomUser model. Handles creation of regular users and superusers.
    """
class CustomUserManager(BaseUserManager):
    """
        Create and return a regular user with an email and password.

        Args:
            email (str): The email address for the user.
            password (str, optional): The password for the user.
            **extra_fields (dict): Additional fields for the user.

        Raises:
            ValueError: If email is not provided.

        Returns:
            CustomUser: The created user.
        """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and return a superuser with an email and password.

        Args:
            email (str): The email address for the superuser.
            password (str): The password for the superuser.
            **extra_fields (dict): Additional fields for the superuser.

        Raises:
            ValueError: If `is_staff` or `is_superuser` is not set to True.

        Returns:
            CustomUser: The created superuser.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


"""
    Custom user model that extends AbstractUser. Uses email as the unique identifier instead of a username.
"""
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("Email Address", max_length=50, unique=True)
    address = models.CharField(max_length=200, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_is_verified = models.BooleanField(default=False)
    selected_movies = models.JSONField(default=list, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """
        Return a string representation of the user, which is the user's email.

        Returns:
            str: The email of the user.
        """
        return self.email
