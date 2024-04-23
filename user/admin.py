from django.contrib import admin
from .forms import UserCreationForm
from user.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "birth_date", "is_active")},
        ),
        ("Address", {"fields": ("address",)}),
        ("Selected Movies", {"fields": ("selected_movies",)}),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
