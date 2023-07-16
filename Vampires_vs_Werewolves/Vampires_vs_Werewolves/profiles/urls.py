from django.urls import path

from Vampires_vs_Werewolves.profiles.views import DetailsUserView

urlpatterns = (
    path('details/', DetailsUserView.as_view(), name='details user'),
)
