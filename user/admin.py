from import_export import resources
from django.contrib import admin
from .forms import UserCreationForm
from user.models import CustomUser
from import_export.admin import ImportExportModelAdmin


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin):
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "birth_date", "is_active","is_staff")},
        ),
        ("Address", {"fields": ("address",)}),
        ("Selected Movies", {"fields": ("selected_movies",)}),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")


class CustomUserResource(resources.ModelResource):

    class Meta:
        model = CustomUser