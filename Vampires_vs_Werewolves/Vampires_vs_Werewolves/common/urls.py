from django.urls import path

from Vampires_vs_Werewolves.common.views import HomeView, RegisterUserView, LoginUserView, LogoutUserView, \
    MarketplaceView, MarketplaceItemView, WorkView, WorkStatusView, CollectMoneyView, BuyItemView, SellItemView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterUserView.as_view(), name='register user'),
    path('login/', LoginUserView.as_view(), name='login user'),
    path('logout/', LogoutUserView.as_view(), name='logout user'),
    path('marketplace/', MarketplaceView.as_view(), name='marketplace'),
    path('marketplace/items/<str:item_type>/', MarketplaceItemView.as_view(), name='item list'),
    path('buy-item/<str:item_type>/<int:item_id>/', BuyItemView.as_view(), name='buy item'),
    path('sell-item/<str:item_type>/<int:item_id>/', SellItemView.as_view(), name='sell item'),
    path('work/', WorkView.as_view(), name='work'),
    path('work/status/<int:work_id>/', WorkStatusView.as_view(), name='work status'),
    path('collect-money/<int:work_id>/', CollectMoneyView.as_view(), name='collect money'),
)
