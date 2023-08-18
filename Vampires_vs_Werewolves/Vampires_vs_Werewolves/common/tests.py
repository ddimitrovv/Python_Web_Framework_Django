from django.test import TestCase
from django.urls import reverse

from Vampires_vs_Werewolves.common.views import HomeView
from Vampires_vs_Werewolves.profiles.models import CustomUser
from django.test import RequestFactory


class HomeViewTest(TestCase):
    def setUp(self):
        # Create a user for testing using the CustomUser model
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.factory = RequestFactory()

    def test_home_view_context(self):
        # Create a request with the logged in user
        request = self.factory.get(reverse('home'))  # Assuming you've named the URL 'home'
        request.user = self.user

        # Use the request to get the response from the view
        response = HomeView.as_view()(request)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the current_user context variable is set correctly
        self.assertEqual(response.context_data['current_user'], self.user)
