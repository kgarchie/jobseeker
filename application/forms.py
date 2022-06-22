from django.contrib.auth.models import User
from django import forms
from .models import User_data


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class AdvancedUser(forms.ModelForm):
    class Meta:
        model = User_data
        fields = ('dob', 'city', 'highQ', 'institution', 'gender', 'dog')


