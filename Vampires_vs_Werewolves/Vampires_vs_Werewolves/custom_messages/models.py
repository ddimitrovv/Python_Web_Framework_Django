from django.db import models

from Vampires_vs_Werewolves.profiles.models import CustomUser


class CustomMessage(models.Model):
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.read = True
        self.save()

    def __str__(self):
        return f"From: {self.sender} | To: {self.recipient} | {self.content[:50]}"
