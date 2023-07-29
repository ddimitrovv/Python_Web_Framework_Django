from django import forms

from Vampires_vs_Werewolves.user_messages.models import CustomMessage


class SendMessageForm(forms.ModelForm):

    class Meta:
        model = CustomMessage
        fields = ['content']


class SendMessageFormChat(forms.ModelForm):

    class Meta:
        model = CustomMessage
        fields = ['content']

        widgets = {
            'content': forms.Textarea(
                attrs={'placeholder': 'Write your message...'}
            ),
        }
        labels = {
            'content': ''
        }
