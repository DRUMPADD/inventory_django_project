from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyCustomUser

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=200,  help_text='Required')

    class Meta:
        model = MyCustomUser
        fields = ('username', 'password', )

