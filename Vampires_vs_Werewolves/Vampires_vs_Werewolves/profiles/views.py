from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import DetailView, UpdateView
from django.db.models import Q

from Vampires_vs_Werewolves.common.models import Work, UserHiding, Attack
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


class UpgradeHeroAttributeView(View, LoginRequiredMixin):
    attribute = None
    cost_multiplier = 1.5

    def get_attribute_value(self, profile):
        raise NotImplementedError("Subclasses must provide a way to get the attribute value")

    def upgrade_attribute(self, profile):
        if profile.gold >= int((self.get_attribute_value(profile) + 1) * self.cost_multiplier):
            profile.gold -= int((self.get_attribute_value(profile) + 1) * self.cost_multiplier)
            setattr(profile, self.attribute, getattr(profile, self.attribute) + 1)
            profile.save()

    def get(self, request, *args, **kwargs):
        profile = get_user_profile(request)
        self.upgrade_attribute(profile)
        return redirect('details user', self.request.user.username)


class UpgradeHeroPowerView(UpgradeHeroAttributeView):
    attribute = 'power'

    def get_attribute_value(self, profile):
        return profile.power


class UpgradeHeroDefenceView(UpgradeHeroAttributeView):
    attribute = 'defence'

    def get_attribute_value(self, profile):
        return profile.defence


class UpgradeHeroSpeedView(UpgradeHeroAttributeView):
    attribute = 'speed'

    def get_attribute_value(self, profile):
        return profile.speed


class ChooseOpponentView(LoginRequiredMixin, View):
    template_name = 'profiles/choose-opponent.html'

    def get(self, request):
        current_user = request.user  # Get the currently authenticated user
        user_profile = current_user.userprofile

        # Check if the user is currently working
        if user_profile.is_working:
            active_work = Work.objects.filter(user=current_user, end_time__isnull=True).first()
            return redirect('work status', active_work.pk)  # Redirect to the work page

        # Check if the user is currently hiding
        if current_user.userprofile.is_hiding:
            hide = UserHiding.objects.filter(user=current_user).first()
            return redirect('stop hiding', hide.pk)

        # Check if user health is less than 15% of it's max health
        if user_profile.health < user_profile.max_health_for_level * 0.15:
            context = {
                'current_user': current_user,
                'user_profile': user_profile,
                'can_fight': False,
            }

            return render(request, self.template_name, context)

        # Get users with the opposite hero type who are within the level range and not hiding
        user_level = user_profile.level
        opponent_type = 'Vampire'if current_user.hero_type == 'Werewolf' else 'Werewolf'
        opponents = UserProfile.objects.filter(
            Q(user__hero_type=opponent_type) &
            Q(level__range=(user_level - 5, user_level + 5)) &
            ~Q(user__userprofile__is_hiding=True)
        ).order_by('?')

        paginator = Paginator(opponents, 3)
        page_number = request.GET.get('page')
        opponents_page = paginator.get_page(page_number)

        context = {
            'current_user': current_user,
            'user_profile': user_profile,
            'opponents': opponents_page,
            'can_fight': True
        }

        return render(request, self.template_name, context)


class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileEditForm()
    template_name = 'profiles/details-profile.html'
    success_url = '/profile/details/'

    def get_object(self, queryset=None):
        user_profile = get_user_profile(self.request)
        return user_profile

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context['form'] = form
        return context


@login_required
def fight_view(request, pk):
    user = request.user
    user_profile = get_user_profile(request)
    opponent = get_object_or_404(UserProfile, user_id=pk)

    # Create or get an Attack instance
    attack, created = Attack.objects.get_or_create(attacker=user, attacked=opponent.user)

    if attack.attacks == 10:
        context = {
            'current_user': get_user_object(request),
            'opponent': opponent,
            'user': user_profile,
            'can_fight': False,
        }
        return render(request, 'profiles/fight-details.html', context)

    # Increment the attack count
    attack.increment_attack_count()
    attack.save()

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
