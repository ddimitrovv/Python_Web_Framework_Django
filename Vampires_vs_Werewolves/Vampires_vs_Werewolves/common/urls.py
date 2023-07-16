from django.urls import path

from Vampires_vs_Werewolves.common.views import HomeView, RegisterUserView, LoginUserView, LogoutUserView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterUserView.as_view(), name='register user'),
    path('login/', LoginUserView.as_view(), name='login user'),
    path('logout/', LogoutUserView.as_view(), name='logout user'),
)
