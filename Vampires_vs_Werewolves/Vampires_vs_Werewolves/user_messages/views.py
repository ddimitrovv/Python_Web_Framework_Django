from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView

from Vampires_vs_Werewolves.user_messages.forms import SendMessageForm
from Vampires_vs_Werewolves.user_messages.models import CustomMessage


class MessageView(LoginRequiredMixin, TemplateView):
    template_name = 'user_messages/messages-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['messages'] = CustomMessage.objects.filter(
            Q(sender=user) | Q(recipient=user)
        )
        context['current_user'] = self.request.user
        context['form'] = SendMessageForm()
        return context


class CreateMessageView(LoginRequiredMixin, CreateView):
    model = CustomMessage
    form_class = SendMessageForm
    template_name = 'user_messages/messages-list.html'
    # success_url = 'details profile'  # Replace with your desired success URL

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)
