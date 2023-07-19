from django import forms

from Vampires_vs_Werewolves.user_messages.models import CustomMessage


class SendMessageForm(forms.ModelForm):
    recipient = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = CustomMessage
        fields = ['recipient', 'content']
