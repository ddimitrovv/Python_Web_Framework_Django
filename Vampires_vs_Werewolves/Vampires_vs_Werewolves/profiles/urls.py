from django.urls import path

from Vampires_vs_Werewolves.profiles.views import DetailsUserView, UpgradeHeroPower, UpgradeHeroDefence, \
    UpgradeHeroSpeed, ChooseOpponentView, fight_view

urlpatterns = (
    path('details/', DetailsUserView.as_view(), name='details user'),
    path('power/', UpgradeHeroPower.as_view(), name='upgrade power'),
    path('defence/', UpgradeHeroDefence.as_view(), name='upgrade defence'),
    path('speed/', UpgradeHeroSpeed.as_view(), name='upgrade speed'),
    path('choose-opponent/', ChooseOpponentView.as_view(), name='choose opponent'),
    path('fight/<int:pk>/', fight_view, name='fight'),
)
