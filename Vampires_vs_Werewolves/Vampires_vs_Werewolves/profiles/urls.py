from django.urls import path

from Vampires_vs_Werewolves.profiles.views import DetailsUserView, UpgradeHeroPowerView, UpgradeHeroDefenceView, \
    UpgradeHeroSpeedView, ChooseOpponentView, fight_view, delete_user_options, delete_user

urlpatterns = (
    path('details/<str:username>/', DetailsUserView.as_view(), name='details user'),
    path('power/', UpgradeHeroPowerView.as_view(), name='upgrade power'),
    path('defence/', UpgradeHeroDefenceView.as_view(), name='upgrade defence'),
    path('speed/', UpgradeHeroSpeedView.as_view(), name='upgrade speed'),
    path('choose-opponent/', ChooseOpponentView.as_view(), name='choose opponent'),
    path('fight/<int:pk>/', fight_view, name='fight'),
    path('delete_user/options/<str:username>/', delete_user_options, name='delete user options'),
    path('delete/<str:username>/', delete_user, name='delete user'),
)
