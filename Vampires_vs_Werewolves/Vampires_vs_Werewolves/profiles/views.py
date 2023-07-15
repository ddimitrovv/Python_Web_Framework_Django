from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from Vampires_vs_Werewolves.profiles.forms import CustomUserRegisterForm
from Vampires_vs_Werewolves.profiles.models import CustomUser


class HomeView(TemplateView):
    template_name = 'common/index.html'


class RegisterUserView(CreateView):
    model = CustomUser
    form_class = CustomUserRegisterForm
    template_name = 'profiles/../../templates/common/register.html'
    success_url = reverse_lazy('home')
