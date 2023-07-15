from django.urls import path

from Vampires_vs_Werewolves.profiles.views import RegisterUserView, HomeView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterUserView.as_view(), name='register user'),
)
