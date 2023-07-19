from django.urls import path

from .views import MessageView, CreateMessageView

urlpatterns = [
    path('', MessageView.as_view(), name='messages'),
    path('create/', CreateMessageView.as_view(), name='create message'),
]
