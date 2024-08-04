from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

"""
    A custom user creation form that extends Django's built-in UserCreationForm.
    Adds additional fields for first name, last name, and birth date.
    """


class UserCreationForm(UserCreationForm):
    firstName = forms.CharField()
    lastName = forms.CharField()
    birthday = forms.CharField()

    def clean(self):
        """
        Adjusts data from frontend to backend by mapping the custom field names to the internal field names.

        This method is called to perform validation and data normalization.

        Returns:
            dict: A dictionary of cleaned data with adjusted field names.
        """
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
        ]
        """
        Meta information for the form that specifies which model it is associated with and
        which fields should be included in the form.

        Attributes:
            model (User): The model associated with this form.
            fields (list): A list of field names to include in the form.
        """
