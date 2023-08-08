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

from Vampires_vs_Werewolves.common.forms import WorkForm
from Vampires_vs_Werewolves.common.models import (Work, HealthPotion, PowerPotion, DefencePotion, SpeedPotion,
                                                  Sword, Shield, Boots)
from Vampires_vs_Werewolves.profiles.forms import UserRegisterForm
from Vampires_vs_Werewolves.profiles.models import CustomUser, UserProfile


class HomeView(TemplateView):
    template_name = 'common/index.html'
    context_object_name = 'current_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            items = item_model.objects.all().order_by('price')

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

    def post(self, request, item_type, item_id):
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


class WorkView(View):
    template_name = 'common/work.html'

    def get(self, request):
        user = request.user
        form = WorkForm()

        if user.userprofile.is_working:
            active_work = Work.objects.filter(user=user, end_time__isnull=True).first()
            return redirect('work status', active_work.pk)  # Redirect to the work page

        context = {
            'current_user': user,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        start_time = timezone.now()
        form = WorkForm(request.POST)

        if form.is_valid():
            hours_worked = int(form.cleaned_data['hours'])
            hourly_wage = user.userprofile.hourly_wage

            active_work = Work.objects.filter(user=user, end_time__isnull=True).first()
            if active_work:
                return redirect('work status', work_id=active_work.id)

            work = Work.objects.create(
                user=user,
                start_time=start_time,
                hourly_wage=hourly_wage,
                hours_worked=hours_worked,
            )

            user.userprofile.is_working = True
            user.userprofile.save()

            return redirect('work status', work_id=work.id)

        context = {
            'user': user,
            'form': form,
        }
        return render(request, self.template_name, context)


class WorkStatusView(View):
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


class CollectMoneyView(View):
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
