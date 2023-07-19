from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import CustomMessage


class AllMessagesView(LoginRequiredMixin, View):
    template_name = 'custom_messages/messages-list.html'

    def get(self, request):
        user = request.user
        messages = CustomMessage.objects.filter(sender=user) | CustomMessage.objects.filter(recipient=user)
        messages = messages.order_by('-timestamp')
        context = {
            'messages': messages,
            'current_user': user
        }
        return render(request, self.template_name, context)
