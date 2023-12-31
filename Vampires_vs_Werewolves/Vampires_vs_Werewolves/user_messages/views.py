from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView

from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from Vampires_vs_Werewolves.profiles.models import CustomUser
from Vampires_vs_Werewolves.user_messages.forms import SendMessageForm, SendMessageFormChat
from Vampires_vs_Werewolves.user_messages.models import CustomMessage
from Vampires_vs_Werewolves.user_messages.serializers import CustomMessageSerializer


class MessageView(LoginRequiredMixin, TemplateView):
    template_name = 'user_messages/messages-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user

        # Get all messages sent or received by the current user, ordered by -timestamp
        messages = CustomMessage.objects.filter(
            Q(sender=current_user) | Q(recipient=current_user)
        ).order_by('-timestamp')

        # Group messages by other user
        grouped_messages = {}
        for message in messages:
            if message.sender != current_user:
                username = message.sender.username
            else:
                username = message.recipient.username

            if username not in grouped_messages:
                grouped_messages[username] = []

            grouped_messages[username].append(message)

        # Check if there are any unread messages for the current user in each group
        for username, user_messages in grouped_messages.items():
            has_unread_messages = any(
                not message.read and message.recipient == current_user for message in user_messages
            )
            user_data = {
                'messages': user_messages,
                'has_unread_messages': has_unread_messages,
            }
            grouped_messages[username] = user_data

        context['current_user'] = current_user
        context['grouped_messages'] = grouped_messages
        return context


class UserMessagesView(LoginRequiredMixin, View):
    template_name = 'user_messages/user-messages.html'

    def get(self, request, username):
        current_user = self.request.user
        other_user = get_object_or_404(CustomUser, username=username)
        other_user_messages = CustomMessage.objects.filter(
            (Q(sender=current_user) & Q(recipient__username=username)) |
            (Q(sender__username=username) & Q(recipient=current_user))
        ).order_by('-timestamp')

        context = {
            'form': SendMessageFormChat(),
            'current_user': current_user,
            'other_user': other_user,
            'messages': other_user_messages,
        }

        for message in other_user_messages:
            if message.recipient == current_user:
                message.read = True
                message.save()

        return render(request, self.template_name, context)

    def post(self, request, username):
        current_user = self.request.user
        form = SendMessageForm(request.POST)

        if form.is_valid():
            recipient = get_object_or_404(CustomUser, username=username)
            message_content = form.cleaned_data.get('content')

            # Create a new message
            CustomMessage.objects.create(
                sender=current_user,
                recipient=recipient,
                content=message_content,
            )

            # Redirect to the user messages view with the updated message list
            return redirect('user messages', username=username)

        # If the form is not valid, render the user messages view with the form and messages
        other_user_messages = CustomMessage.objects.filter(
            (Q(sender=current_user) & Q(recipient__username=username)) |
            (Q(sender__username=username) & Q(recipient=current_user))
        ).order_by('-timestamp')

        context = {
            'form': form,
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


class EditMessageAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomMessage.objects.all()
    serializer_class = CustomMessageSerializer

    def put(self, request, *args, **kwargs):
        current_message_pk = self.kwargs.get('pk')
        current_message = self.queryset.filter(pk=current_message_pk).first()
        if current_message is None:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(current_message, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {
            'updated_message': serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class DeleteMessageAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        current_message_pk = self.kwargs.get('pk')
        current_message = CustomMessage.objects.get(pk=current_message_pk)

        if current_message is None:
            response = Response(
                {'error': 'Message not found'},
                status=status.HTTP_404_NOT_FOUND,
                content_type='application/json'
            )
            print(response)
            return response

        self.perform_destroy(current_message)
        response = Response(
            {'message': 'Message deleted successfully'},
            status=status.HTTP_204_NO_CONTENT,
            content_type='application/json'
        )
        print(response)
        return response

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        response['content-type'] = 'application/json'
        return response
