from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from Vampires_vs_Werewolves.profiles.forms import UserRegisterForm
from Vampires_vs_Werewolves.profiles.models import CustomUser


class RegisterUserView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'common/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class LoginUserView(LoginView):
    template_name = 'common/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUserView(LogoutView, LoginRequiredMixin):
    next_page = '/'
