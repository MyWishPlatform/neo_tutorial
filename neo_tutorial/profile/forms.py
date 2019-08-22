from django import forms
from django.contrib.auth.forms import UserCreationForm
from neo_tutorial.profile.models import TutorialUser


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = TutorialUser
        fields = ('username', 'email', 'password1', 'password2')
