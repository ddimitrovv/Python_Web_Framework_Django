from rest_framework import serializers

from Vampires_vs_Werewolves.user_messages.models import CustomMessage


class CustomMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMessage
        fields = '__all__'
