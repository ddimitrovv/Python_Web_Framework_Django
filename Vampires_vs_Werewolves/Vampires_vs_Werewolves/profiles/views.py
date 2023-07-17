from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView, TemplateView
from Vampires_vs_Werewolves.profiles.models import CustomUser, UserProfile


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
        print(pk)
        current_user = UserProfile.objects.filter(user_id=pk).get()
        context['profile'] = current_user
        return context


class UpgradeHeroPower(UpdateView, LoginRequiredMixin):
    def get_object(self, queryset=None):
        return self.request.user or None

    def get(self, request, *args, **kwargs):
        username = self.get_object()
        user = CustomUser.objects.filter(username=username).get()
        profile = UserProfile.objects.filter(user_id=user.pk).get()
        if profile.gold >= (profile.power + 1) * 1.5:
            profile.gold -= (profile.power + 1) * 1.5
            profile.power += 1
            profile.save()
        return redirect('details user')


class UpgradeHeroDefence(UpdateView, LoginRequiredMixin):
    def get_object(self, queryset=None):
        return self.request.user or None

    def get(self, request, *args, **kwargs):
        username = self.get_object()
        user = CustomUser.objects.filter(username=username).get()
        profile = UserProfile.objects.filter(user_id=user.pk).get()
        if profile.gold >= (profile.defence + 1) * 1.5:
            profile.gold -= (profile.defence + 1) * 1.5
            profile.defence += 1
            profile.save()
        return redirect('details user')


class UpgradeHeroSpeed(UpdateView, LoginRequiredMixin):
    def get_object(self, queryset=None):
        return self.request.user or None

    def get(self, request, *args, **kwargs):
        username = self.get_object()
        user = CustomUser.objects.filter(username=username).get()
        profile = UserProfile.objects.filter(user_id=user.pk).get()
        if profile.gold >= (profile.speed + 1) * 1.5:
            profile.gold -= (profile.speed + 1) * 1.5
            profile.speed += 1
            profile.save()
        return redirect('details user')


class ChooseOpponentView(TemplateView, LoginRequiredMixin):
    template_name = 'profiles/choose-opponent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)

        user = self.request.user  # Get the currently authenticated user
        user_profile = user.userprofile

        # Get users by hero type
        hero_type_ = 'Vampire' if user.hero_type == 'Werewolf' else 'Werewolf'
        users = CustomUser.objects.filter(hero_type=hero_type_)

        # Filter profiles by level within the specified range
        opponents = UserProfile.objects.filter(user__in=users, level__range=(user_profile.level - 5, user_profile.level + 5)).order_by('?')[:10]

        context['user_profile'] = user_profile
        context['opponents'] = opponents

        return context
