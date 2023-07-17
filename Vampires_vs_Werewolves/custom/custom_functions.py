from django.shortcuts import get_object_or_404
from Vampires_vs_Werewolves.profiles.models import CustomUser, UserProfile


def get_user_object(request):
    username = request.user
    return get_object_or_404(CustomUser, username=username)


def get_user_profile(request):
    user = get_user_object(request)
    return get_object_or_404(UserProfile, user=user)
