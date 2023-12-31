from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.db.models import F

from Vampires_vs_Werewolves.common.forms import WorkForm
from Vampires_vs_Werewolves.common.models import (Work, HealthPotion, PowerPotion, DefencePotion, SpeedPotion,
                                                  Sword, Shield, Boots, UserHiding)
from Vampires_vs_Werewolves.profiles.forms import UserRegisterForm
from Vampires_vs_Werewolves.profiles.tasks import remove_bonus
from Vampires_vs_Werewolves.profiles.models import CustomUser, UserProfile
from Vampires_vs_Werewolves.user_messages.models import CustomMessage


class HomeView(TemplateView):
    template_name = 'common/index.html'
    context_object_name = 'current_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        if current_user.is_authenticated:
            received_messages = CustomMessage.objects.filter(recipient=current_user).order_by('-timestamp')
            has_unread_messages = any(not message.read for message in received_messages)
            context['has_unread_messages'] = has_unread_messages
        context['current_user'] = self.request.user

        return context


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
        return reverse_lazy('details user', kwargs={'username': self.request.user.username})


class LogoutUserView(LogoutView, LoginRequiredMixin):
    next_page = 'home'


class MarketplaceView(LoginRequiredMixin, TemplateView):
    template_name = 'common/marketplace.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['user_profile'] = get_object_or_404(UserProfile, user_id=self.request.user.pk)
        return context


class MarketplaceItemView(LoginRequiredMixin, TemplateView):
    template_name = 'common/items-list.html'
    model_map = {
        'swords': Sword,
        'shields': Shield,
        'boots': Boots,
        'health_potions': HealthPotion,
        'power_potions': PowerPotion,
        'defence_potions': DefencePotion,
        'speed_potions': SpeedPotion,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_type = kwargs['item_type']
        item_model = self.model_map.get(item_type)

        if item_model is None:
            raise Http404("Item type does not exist")

        if item_type in ['swords', 'shields', 'boots']:
            items = item_model.objects.all().order_by('required_level')
        else:
            items = item_model.objects.all().order_by('hours_active', 'percent_bonus')

        paginator = Paginator(items, 3)
        page_number = self.request.GET.get('page')
        items_page = paginator.get_page(page_number)

        context['current_user'] = self.request.user
        context['user_profile'] = get_object_or_404(UserProfile, user_id=self.request.user.pk)
        context['items'] = items_page
        return context


class BuyItemView(LoginRequiredMixin, View):
    item_models = {
        'sword': Sword,
        'shield': Shield,
        'boots': Boots,
        'healthpotion': HealthPotion,
        'powerpotion': PowerPotion,
        'defencepotion': DefencePotion,
        'speedpotion': SpeedPotion,
    }

    item_fields = {
        'sword': 'sword',
        'shield': 'shield',
        'boots': 'boots',
        'healthpotion': 'health_potion',
        'powerpotion': 'power_potion',
        'defencepotion': 'defence_potion',
        'speedpotion': 'speed_potion',
    }

    def post(self, request, item_type, item_id):
        user_profile = get_object_or_404(UserProfile, user=request.user)

        # Check if the user is already equipped with an item of the same type
        equipped_item_field = self.item_fields.get(item_type)
        if equipped_item_field and getattr(user_profile, equipped_item_field):
            return redirect('marketplace')

        item_model = self.item_models.get(item_type)
        if not item_model:
            return redirect('marketplace')

        item = get_object_or_404(item_model, pk=item_id)

        if (user_profile.gold < item.price or
                (hasattr(item, 'required_level') and user_profile.level < item.required_level)):
            return redirect('marketplace')

        # Multiply the price by hero level for potions
        if 'potion' in item_type:
            item.price *= user_profile.level

        user_profile.gold -= item.price

        if equipped_item_field:
            setattr(user_profile, equipped_item_field, item)

        user_profile.save()

        return redirect('details user', user_profile.user.username)


class SellItemView(LoginRequiredMixin, View):
    item_model_mapping = {
        'sword': Sword,
        'shield': Shield,
        'boots': Boots,
    }

    def post(self, request, item_type):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        item_model = self.item_model_mapping.get(item_type)

        if not item_model:
            return redirect('details user', user_profile.user.username)

        # item = get_object_or_404(item_model, pk=item_id)
        item_attribute_name = item_type

        if not hasattr(user_profile, item_attribute_name):
            return redirect('details user', user_profile.user.username)

        old_item = getattr(user_profile, item_attribute_name)
        user_profile.gold += old_item.sell_price

        setattr(user_profile, item_attribute_name, None)
        user_profile.save()

        return redirect('details user', user_profile.user.username)


class WorkView(LoginRequiredMixin, View):
    template_name = 'common/work.html'

    def get(self, request):
        current_user = request.user
        form = WorkForm()

        if current_user.userprofile.is_hiding:
            hide = UserHiding.objects.filter(user=current_user).first()
            return redirect('stop hiding', hide.pk)

        if current_user.userprofile.is_working:
            active_work = Work.objects.filter(user=current_user, end_time__isnull=True).first()
            return redirect('work status', active_work.pk)  # Redirect to the work page

        context = {
            'current_user': current_user,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        current_user = request.user
        start_time = timezone.now()
        form = WorkForm(request.POST)

        if form.is_valid():
            hours_worked = int(form.cleaned_data['hours'])
            hourly_wage = current_user.userprofile.hourly_wage

            active_work = Work.objects.filter(user=current_user, end_time__isnull=True).first()
            if active_work:
                return redirect('work status', work_id=active_work.id)

            work = Work.objects.create(
                user=current_user,
                start_time=start_time,
                hourly_wage=hourly_wage,
                hours_worked=hours_worked,
            )

            current_user.userprofile.is_working = True
            current_user.userprofile.save()

            return redirect('work status', work_id=work.id)

        context = {
            'user': current_user,
            'form': form,
        }
        return render(request, self.template_name, context)


class WorkStatusView(LoginRequiredMixin, View):
    template_name = 'common/work-status.html'

    def get(self, request, work_id):
        work = get_object_or_404(Work, id=work_id)
        current_time = timezone.now()
        time_difference = current_time - work.start_time
        remaining_hours = work.hours_worked - int(time_difference.total_seconds() // 3600)
        # Calculate the amount of money earned based on the hours worked
        hourly_wage = work.user.userprofile.hourly_wage
        start_time = work.start_time
        hours_worked = (current_time - start_time).seconds // 3600
        earned_money = hourly_wage * hours_worked \
            if hours_worked <= work.hours_worked \
            else hourly_wage * work.hours_worked

        context = {
            'work': work,
            'remaining_hours': remaining_hours,
            'money_earned': earned_money,
            'current_user': self.request.user
        }

        return render(request, self.template_name, context)


class CollectMoneyView(LoginRequiredMixin, View):
    def get(self, request, work_id):
        # Get the work entry with the specified ID
        try:
            work = Work.objects.get(id=work_id, user=request.user, end_time__isnull=True)
        except Work.DoesNotExist:
            # If the work entry does not exist or has already ended, redirect to home
            return redirect('home')

        # Calculate the amount of money earned based on the hours worked
        hourly_wage = work.user.userprofile.hourly_wage
        start_time = work.start_time
        current_time = timezone.now()
        hours_worked = (current_time - start_time).seconds // 3600
        earned_money = hourly_wage * hours_worked \
            if hours_worked <= work.hours_worked \
            else hourly_wage * work.hours_worked

        # Set the end time to the current time
        work.end_time = current_time
        work.hours_worked = hours_worked
        work.save()

        # Update the user's gold with the earned money
        user_profile = work.user.userprofile
        user_profile.gold += earned_money
        user_profile.is_working = False
        user_profile.save()
        return redirect('home')


class HideUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        current_user = request.user

        if current_user.userprofile.is_hiding:
            hide = UserHiding.objects.filter(user=current_user).first()
            return redirect('stop hiding', hide.pk)

        # Render the template for showing hide user details
        return render(request, 'common/hiding.html', {'current_user': current_user})

    def post(self, request, *args, **kwargs):
        current_user = request.user
        user_profile = current_user.userprofile

        if not user_profile.is_hiding:
            UserHiding.objects.create(user=current_user)
            user_profile.is_hiding = True
            user_profile.save()

        hide = UserHiding.objects.filter(user=current_user).first()
        return redirect('stop hiding', hide.pk)


class StopHidingView(LoginRequiredMixin, View):
    template_name = 'common/hiding-details.html'  # Replace with the actual template name

    def get(self, request, pk):
        current_user = request.user
        user_profile = current_user.userprofile
        hiding_details = UserHiding.objects.get(id=pk)

        # Calculate whether it's time to stop hiding
        stop_hiding = hiding_details.can_stop_hiding_at <= timezone.now()

        context = {
            'current_user': current_user,
            'user_profile': user_profile,
            'hiding_details': hiding_details,
            'stop_hiding': stop_hiding,
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        hiding_details = UserHiding.objects.get(id=pk)

        if hiding_details.can_stop_hiding_at and hiding_details.can_stop_hiding_at <= timezone.now():
            # Stop hiding and update user's hiding status
            user_profile = hiding_details.user.userprofile
            hiding_details.delete()
            user_profile.is_hiding = False
            user_profile.save()

        return redirect('home')


class InventoryView(LoginRequiredMixin, TemplateView):
    template_name = 'common/inventory.html'

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        user_profile = get_object_or_404(UserProfile, user_id=self.request.user.pk)

        items = [
            user_profile.sword,
            user_profile.shield,
            user_profile.boots,
            user_profile.health_potion,
            user_profile.power_potion,
            user_profile.defence_potion,
            user_profile.speed_potion,
        ]

        actual_items = [item for item in items if item is not None]

        paginator = Paginator(actual_items, 3)
        page_number = self.request.GET.get('page')
        items_page = paginator.get_page(page_number)
        context = {'current_user': current_user,
                   'user_profile': user_profile,
                   'items': items_page}
        return context


class ActivatePotionView(LoginRequiredMixin, View):
    def post(self, request, potion_type):
        current_user = request.user
        user_profile = request.user.userprofile

        potion_types = {
            'Health': 'health_potion',
            'Power': 'power_potion',
            'Defence': 'defence_potion',
            'Speed': 'speed_potion',
        }

        field_to_add_bonus = {
            'Health': 'health',
            'Power': 'power_bonus',
            'Defence': 'defence_bonus',
            'Speed': 'speed_bonus',
        }

        field_to_get_value_from = {
            'Health': 'health',
            'Power': 'power',
            'Defence': 'defence',
            'Speed': 'speed',
        }

        current_potion_type = potion_types[potion_type]
        current_potion = getattr(user_profile, current_potion_type)
        bonus = current_potion.percent_bonus / 100

        if potion_type != 'Health':
            field_to_update = field_to_add_bonus.get(potion_type)
            actual_value = getattr(user_profile, field_to_get_value_from.get(potion_type))
            bonus_value = getattr(user_profile, field_to_update)

            if bonus_value != 0:
                return redirect('inventory', current_user.username)

            new_value = round(actual_value * bonus)
            setattr(user_profile, field_to_update, new_value)

            # Schedule the Celery task to remove bonus
            remove_bonus.apply_async(args=[user_profile.id, field_to_update],
                                     countdown=current_potion.hours_active * 3600)
        elif potion_type == 'Health':
            max_health = user_profile.max_health_for_level
            user_profile.health += min(round(max_health * bonus), user_profile.max_health_for_level)

        setattr(user_profile, current_potion_type, None)
        user_profile.save()

        return redirect('details user', current_user.username)


class RankingView(LoginRequiredMixin, TemplateView):
    template_name = 'common/ranking.html'
    paginate_by = 10  # Number of players per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate the difference between wins and losses
        all_players = UserProfile.objects.annotate(win_loss_diff=F('wins') - F('losses'))

        # Order players by the calculated win-loss difference and then by level
        all_players = all_players.order_by('-win_loss_diff', '-level')

        # Paginate the players
        paginator = Paginator(all_players, self.paginate_by)
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)

        context.update({
            'players': page,
            'current_user': self.request.user
        })

        return context
