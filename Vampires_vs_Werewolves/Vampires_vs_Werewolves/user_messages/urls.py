from django.urls import path

from .views import MessageView, CreateMessageView, UserMessagesView

urlpatterns = [
    path('', MessageView.as_view(), name='messages'),
    path('create/<str:username>', CreateMessageView.as_view(), name='create message'),
    path('<str:username>/', UserMessagesView.as_view(), name='user messages'),
]
