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
    ResetPasswordView,
    SignUp,
    password_reset_email_sent,
    get_csrf_token
)
from movie_town_backend import settings
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('api/csrf-token/',get_csrf_token, name='get_csrf_token'),
    path("django-rq/", include("django_rq.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', admin.site.urls),
    path("admin/", admin.site.urls),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", SignUp.as_view(), name="signup"),
    path("current_user/", CurrentUser.as_view()),
    path("movie_select/", Movie_Select.as_view()),
    path("video/", Video.as_view(), name="video"),
    path("video/<int:user_id>/", Video.as_view()),
    path("video/<int:user_id>/<int:movie_id>/", Video.as_view()),
    path("verification/", include("verify_email.urls")),
    path("password_reset/", ResetPasswordView.as_view()),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "password_reset_email_sent/",
        password_reset_email_sent,
        name="password_reset_email_sent",
    ),
] + staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
