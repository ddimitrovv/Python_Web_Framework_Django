from django.urls import path

from .views import MessageView, CreateMessageView, UserMessagesView, EditMessageAPIView

urlpatterns = [
    path('', MessageView.as_view(), name='messages'),
    path('create/<str:username>', CreateMessageView.as_view(), name='create message'),
    path('<str:username>/', UserMessagesView.as_view(), name='user messages'),
    path('edit-message/<int:pk>/', EditMessageAPIView.as_view(), name='edit message'),
]
