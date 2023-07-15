from django import forms
from django.contrib.auth.forms import UserCreationForm

from Vampires_vs_Werewolves.profiles.models import CustomUser


class CustomUserRegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password'}), label='Type password:')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password'}), label='Retype password:')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'hero_type')
