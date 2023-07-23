from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Vampires_vs_Werewolves.common.urls')),
    path('profile/', include('Vampires_vs_Werewolves.profiles.urls')),
    path('messages/', include('Vampires_vs_Werewolves.user_messages.urls')),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)