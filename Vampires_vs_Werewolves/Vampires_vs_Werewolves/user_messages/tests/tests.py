from django.test import TestCase
from Vampires_vs_Werewolves.profiles.models import CustomUser
from Vampires_vs_Werewolves.user_messages.models import CustomMessage


class CustomMessageModelTest(TestCase):

    def setUp(self):
        self.sender = CustomUser.objects.create(username='sender', email='sender@example.com')
        self.recipient = CustomUser.objects.create(username='recipient', email='recipient@example.com')
        self.message = CustomMessage.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            content='Hello, this is a test message.'
        )

    def test_mark_as_read(self):
        self.assertFalse(self.message.read)
        self.message.mark_as_read()
        self.assertTrue(self.message.read)

    def test_str_representation(self):
        expected_str = f"From: {self.sender} | To: {self.recipient} | Hello, this is a test message."
        self.assertEqual(str(self.message), expected_str)

    def test_sender_related_name(self):
        self.assertEqual(self.sender.sent_messages.first(), self.message)

    def test_recipient_related_name(self):
        self.assertEqual(self.recipient.received_messages.first(), self.message)

    def test_timestamp_auto_add(self):
        # Create a new message and check if timestamps are different
        new_message = CustomMessage.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            content='Another test message.'
        )
        self.assertNotEqual(self.message.timestamp, new_message.timestamp)
