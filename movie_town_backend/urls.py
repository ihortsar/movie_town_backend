"""
URL configuration for movie_town_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from movies.views import Video
from user.views import (
    CurrentUser,
    CustomLoginView,
    Movie_Select,
    PasswordResetConfirmView,
    ResetPasswordView,
    SignUp,
)
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("django-rq/", include("django_rq.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", SignUp.as_view(), name="signup"),
    path("current_user/", CurrentUser.as_view(), name="current_user"),
    path("movie_select/", Movie_Select.as_view()),
    path("video/", Video.as_view(), name="video"),
    path("video/<int:user_id>/", Video.as_view(), name="video_with_user"),
    path(
        "video/<int:user_id>/<int:movie_id>/",
        Video.as_view(),
        name="video_with_user_movie",
    ),
    path("verification/", include("verify_email.urls")),
    path("password_reset/", ResetPasswordView.as_view()),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
] + staticfiles_urlpatterns()


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
