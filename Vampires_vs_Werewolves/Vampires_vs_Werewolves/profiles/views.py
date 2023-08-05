from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import DetailView, UpdateView

from Vampires_vs_Werewolves.common.models import Work
from Vampires_vs_Werewolves.profiles.forms import UserProfileEditForm
from Vampires_vs_Werewolves.profiles.models import CustomUser, UserProfile
from custom.custom_functions import get_user_profile, get_user_object
from Vampires_vs_Werewolves.profiles.tasks import start_healing

class DetailsUserView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profiles/details-profile.html'
    context_object_name = 'user'
    login_url = '/profile/login/'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(self.model, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object.userprofile
        context['profile'] = user
        context['current_user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.gender = 'Female' if user_profile.gender == 'Male' else 'Male'
        user_profile.save()
        return redirect('details user', self.request.user.username)


class UpgradeHeroPower(UpdateView, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        profile = get_user_profile(request)
        if profile.gold >= int((profile.power + 1) * 1.5):
            profile.gold -= int((profile.power + 1) * 1.5)
            profile.power += 1
            profile.save()
        return redirect('details user', self.request.user.username)


class UpgradeHeroDefence(UpdateView, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        profile = get_user_profile(request)
        if profile.gold >= int((profile.defence + 1) * 1.5):
            profile.gold -= int((profile.defence + 1) * 1.5)
            profile.defence += 1
            profile.save()
        return redirect('details user', self.request.user.username)


class UpgradeHeroSpeed(UpdateView, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        profile = get_user_profile(request)
        if profile.gold >= int((profile.speed + 1) * 1.5):
            profile.gold -= int((profile.speed + 1) * 1.5)
            profile.speed += 1
            profile.save()
        return redirect('details user', self.request.user.username)


class ChooseOpponentView(LoginRequiredMixin, View):
    template_name = 'profiles/choose-opponent.html'

    def get(self, request):
        user = request.user  # Get the currently authenticated user
        user_profile = user.userprofile

        # Check if the user is currently working
        if user_profile.is_working:
            active_work = Work.objects.filter(user=user, end_time__isnull=True).first()
            return redirect('work status', active_work.pk)  # Redirect to the work page

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
        ).order_by('?')

        paginator = Paginator(opponents, 3)
        page_number = request.GET.get('page')
        opponents_page = paginator.get_page(page_number)

        context = {
            'current_user': user,
            'user_profile': user_profile,
            'opponents': opponents_page,
        }

        return render(request, self.template_name, context)


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


# def fight_view(request, pk):
#     user_profile = get_user_profile(request)
#     opponent = UserProfile.objects.get(user_id=pk)
#     winner = user_profile.fight(opponent)
#
#     context = {
#         'current_user': get_user_object(request),
#         'opponent': opponent,
#         'winner': winner,
#         'user': user_profile
#     }
#
#     return render(request, 'profiles/fight-details.html', context)
def fight_view(request, pk):
    user = request.user
    user_profile = get_user_profile(request)
    opponent = get_object_or_404(UserProfile, user_id=pk)

    winner = user_profile.fight(opponent)

    # Check if health is below max_health, and start healing asynchronously
    if user_profile.health < user_profile.max_health_for_level and not user_profile.is_healing:
        start_healing.delay(user.id)

    if opponent.health < opponent.max_health_for_level and not opponent.is_healing:
        start_healing.delay(opponent.id)

    context = {
        'current_user': get_user_object(request),
        'opponent': opponent,
        'winner': winner,
        'user': user_profile
    }

    return render(request, 'profiles/fight-details.html', context)

