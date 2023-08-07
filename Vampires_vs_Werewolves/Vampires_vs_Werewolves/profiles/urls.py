from django.urls import path

from Vampires_vs_Werewolves.profiles.views import DetailsUserView, UpgradeHeroPowerView, UpgradeHeroDefenceView, \
    UpgradeHeroSpeedView, ChooseOpponentView, fight_view

urlpatterns = (
    path('details/<str:username>/', DetailsUserView.as_view(), name='details user'),
    path('power/', UpgradeHeroPowerView.as_view(), name='upgrade power'),
    path('defence/', UpgradeHeroDefenceView.as_view(), name='upgrade defence'),
    path('speed/', UpgradeHeroSpeedView.as_view(), name='upgrade speed'),
    path('choose-opponent/', ChooseOpponentView.as_view(), name='choose opponent'),
    path('fight/<int:pk>/', fight_view, name='fight'),
)
