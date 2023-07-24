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

from .forms import WorkForm
from .models import Work
from django.utils import timezone

from Vampires_vs_Werewolves.common.models import Sword, Shield, Boots
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
        return context


class MarketplaceItemView(LoginRequiredMixin, TemplateView):
    template_name = 'common/items-list.html'
    model_map = {
        'swords': Sword,
        'shields': Shield,
        'boots': Boots,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_type = kwargs['item_type']
        item_model = self.model_map.get(item_type)

        if item_model is None:
            raise Http404("Item type does not exist")

        items = item_model.objects.all()

        paginator = Paginator(items, 3)
        page_number = self.request.GET.get('page')
        items_page = paginator.get_page(page_number)

        context['current_user'] = self.request.user
        context['items'] = items_page
        return context


class BuyItemView(LoginRequiredMixin, View):
    def post(self, request, item_type, item_id):
        user_profile = get_object_or_404(UserProfile, user=request.user)

        # Check if the user is already equipped with an item of the same type
        if item_type == 'sword' and user_profile.sword:
            return redirect('marketplace')
        elif item_type == 'shield' and user_profile.shield:
            return redirect('marketplace')
        elif item_type == 'boots' and user_profile.boots:
            return redirect('marketplace')

        item_model = None
        if item_type == 'sword':
            item_model = Sword
        elif item_type == 'shield':
            item_model = Shield
        elif item_type == 'boots':
            item_model = Boots

        if item_model is None:
            return redirect('marketplace')

        item = get_object_or_404(item_model, pk=item_id)

        # Check if the user has enough gold to buy the item
        if user_profile.gold < item.price or user_profile.level < item.required_level:
            return redirect('marketplace')

        user_profile.gold -= item.price

        if item_type == 'sword':
            user_profile.sword = item
        elif item_type == 'shield':
            user_profile.shield = item
        elif item_type == 'boots':
            user_profile.boots = item

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
                hours_worked=hours_worked,
                hourly_wage=hourly_wage)

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
        money_earned = work.hourly_wage * (work.hours_worked - remaining_hours)

        context = {
            'work': work,
            'remaining_hours': remaining_hours,
            'money_earned': money_earned,
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
        earned_money = hourly_wage * hours_worked

        # Set the end time to the current time
        work.end_time = current_time
        work.save()

        # Update the user's gold with the earned money
        user_profile = work.user.userprofile
        user_profile.gold += earned_money
        user_profile.is_working = False
        user_profile.save()

        return redirect('home')
