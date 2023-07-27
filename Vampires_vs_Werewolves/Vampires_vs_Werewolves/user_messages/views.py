from itertools import groupby

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView

from Vampires_vs_Werewolves.profiles.models import CustomUser
from Vampires_vs_Werewolves.user_messages.forms import SendMessageForm
from Vampires_vs_Werewolves.user_messages.models import CustomMessage


class MessageView(LoginRequiredMixin, TemplateView):
    template_name = 'user_messages/messages-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user

        # Get all messages sent or received by the current user
        messages = CustomMessage.objects.filter(
            Q(sender=current_user) | Q(recipient=current_user)
        ).order_by('-timestamp')

        # Group messages by sender's username different from the current user
        grouped_messages = {}
        for username, group in groupby(
                messages,
                key=lambda m: m.sender.username if m.sender != current_user else m.recipient.username
        ):
            grouped_messages[username] = list(group)

        context['current_user'] = current_user
        context['grouped_messages'] = grouped_messages
        return context


class UserMessagesView(LoginRequiredMixin, View):
    template_name = 'user_messages/user-messages.html'

    def get(self, request, username):
        current_user = self.request.user
        other_user_messages = CustomMessage.objects.filter(
            (Q(sender=current_user) & Q(recipient__username=username)) |
            (Q(sender__username=username) & Q(recipient=current_user))
        ).order_by('-timestamp')
        context = {
            'current_user': current_user,
            'other_user': username,
            'messages': other_user_messages,
        }
        return render(request, self.template_name, context)


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
        context['recipient_username'] = self.kwargs.get('username')
        return context
