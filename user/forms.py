from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserCreationForm(UserCreationForm):
    firstName = forms.CharField()
    lastName = forms.CharField()
    birthday = forms.CharField()

    def clean(self):
        # Adjusts data from frontend to backend
        cleaned_data = super().clean()
        first_name = cleaned_data.get("firstName")
        last_name = cleaned_data.get("lastName")
        birth_date = cleaned_data.get("birthday")
        cleaned_data["first_name"] = first_name
        cleaned_data["last_name"] = last_name
        cleaned_data["birth_date"] = birth_date
        return cleaned_data

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "password1",
            "password2",
        ]  # fields that are required to create a user
