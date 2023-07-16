from django.urls import path

from Vampires_vs_Werewolves.common.views import HomeView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
)
