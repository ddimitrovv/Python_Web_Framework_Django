from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, UpdateView, TemplateView

from Vampires_vs_Werewolves.profiles.forms import UserProfileEditForm
from Vampires_vs_Werewolves.profiles.models import CustomUser, UserProfile
from custom.custom_functions import get_user_profile


class DetailsUserView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profiles/details-profile.html'
    context_object_name = 'user'
    login_url = '/profile/login/'

    def get_object(self, queryset=None):
        return self.request.user or None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.request.user.pk
        current_user = UserProfile.objects.filter(user_id=pk).get()
        context['profile'] = current_user
        return context

    def post(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.gender = 'Female' if user_profile.gender == 'Male' else 'Male'
        user_profile.save()
        return redirect('details user')


class UpgradeHeroPower(UpdateView, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        profile = get_user_profile(request)
        if profile.gold >= int((profile.power + 1) * 1.5):
            profile.gold -= int((profile.power + 1) * 1.5)
            profile.power += 1
            profile.save()
        return redirect('details user')


class UpgradeHeroDefence(UpdateView, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        profile = get_user_profile(request)
        if profile.gold >= int((profile.defence + 1) * 1.5):
            profile.gold -= int((profile.defence + 1) * 1.5)
            profile.defence += 1
            profile.save()
        return redirect('details user')


class UpgradeHeroSpeed(UpdateView, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        profile = get_user_profile(request)
        if profile.gold >= int((profile.speed + 1) * 1.5):
            profile.gold -= int((profile.speed + 1) * 1.5)
            profile.speed += 1
            profile.save()
        return redirect('details user')


class ChooseOpponentView(TemplateView, LoginRequiredMixin):
    template_name = 'profiles/choose-opponent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user  # Get the currently authenticated user
        user_profile = user.userprofile

        # Get users by hero type
        hero_type_ = 'Vampire' if user.hero_type == 'Werewolf' else 'Werewolf'
        users = CustomUser.objects.filter(hero_type=hero_type_)

        # Filter profiles by level within the specified range
        opponents = UserProfile.objects.filter(
            user__in=users,
            level__range=(
               user_profile.level - 5,
               user_profile.level + 5
            )
        ).order_by('?')[:10]

        context['user_profile'] = user_profile
        context['opponents'] = opponents

        return context


class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileEditForm()
    template_name = 'profiles/details-profile.html'
    success_url = '/profile/details/'

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context['form'] = form
        return context


def fight_view(request, pk):
    user_profile = get_user_profile(request)
    opponent = UserProfile.objects.get(user_id=pk)
    winner = user_profile.fight(opponent)

    context = {
        'opponent': opponent,
        'winner': winner
    }

    return render(request, 'profiles/fight-details.html', context)

