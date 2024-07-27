from import_export import resources
from django.contrib import admin
from .forms import UserCreationForm
from user.models import CustomUser
from import_export.admin import ImportExportModelAdmin


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin):
    """Admin interface for the CustomUser model with import/export capabilities.
    This class customizes the Django admin interface for managing `CustomUser` instances.
    It also integrates with `django-import-export` to provide data import and export functionality.
    """

    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "birth_date",
                    "is_active",
                    "is_staff",
                )
            },
        ),
        ("Address", {"fields": ("address",)}),
        ("Selected Movies", {"fields": ("selected_movies",)}),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")


class CustomUserResource(resources.ModelResource):
    """
    Resource class for exporting and importing `CustomUser` instances using django-import-export.

    This class is used to define how the `CustomUser` model should be represented
    when importing from or exporting to various data formats (e.g., CSV, XLSX).
    """

    class Meta:
        model = CustomUser
