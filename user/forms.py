from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserCreationForm(UserCreationForm):
    password = forms.CharField(label="Password")
    firstName = forms.CharField(label="First Name") 
    lastName = forms.CharField(label="Last Name") 
    birthday = forms.CharField(label="Bithdate") 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].required = False
        self.fields[
            "password2"
        ].required = False  # remove from default required in forms

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['first_name'] = cleaned_data.get('firstName')
        cleaned_data['last_name'] = cleaned_data.get('lastName')
        cleaned_data['birth_date'] = cleaned_data.get('birthday') # adjust data from frontend to backend
        return cleaned_data

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "birth_date",
        ]  # fields that are required to create a user