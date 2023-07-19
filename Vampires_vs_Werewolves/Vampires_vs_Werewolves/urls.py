from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Vampires_vs_Werewolves.common.urls')),
    path('profile/', include('Vampires_vs_Werewolves.profiles.urls')),
    path('all-messages/', include('Vampires_vs_Werewolves.custom_messages.urls')),
]
