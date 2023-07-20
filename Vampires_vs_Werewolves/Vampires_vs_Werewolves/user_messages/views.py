from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from Vampires_vs_Werewolves.profiles.models import UserProfile, CustomUser
from Vampires_vs_Werewolves.user_messages.forms import SendMessageForm
from Vampires_vs_Werewolves.user_messages.models import CustomMessage


class MessageView(LoginRequiredMixin, TemplateView):
    template_name = 'user_messages/messages-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        messages = CustomMessage.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).order_by('-timestamp')
        # context['messages'] = CustomMessage.objects.filter(
        #     Q(sender=user) | Q(recipient=user)
        # ).order_by('-timestamp')
        context['current_user'] = self.request.user
        context['form'] = SendMessageForm()
        paginator = Paginator(messages, 4)
        page_number = self.request.GET.get('page')
        messages_page = paginator.get_page(page_number)
        context['messages'] = messages_page
        return context


class CreateMessageView(LoginRequiredMixin, CreateView):
    model = CustomMessage
    form_class = SendMessageForm
    template_name = 'user_messages/create-message.html'
    success_url = reverse_lazy('messages')  # Replace with your desired success URL

    def form_valid(self, form):
        form.instance.sender = self.request.user
        recipient_username = self.kwargs.get('username')
        recipient = get_object_or_404(CustomUser, username=recipient_username)
        form.instance.recipient = recipient
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['current_user'] = user
        return context
