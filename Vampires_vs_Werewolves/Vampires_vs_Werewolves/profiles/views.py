from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from Vampires_vs_Werewolves.profiles.models import CustomUser, UserProfile


class DetailsUserView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profiles/details-profile.html'
    context_object_name = 'user'
    login_url = '/profile/login/'

    def get_object(self, queryset=None):
        return self.request.user or None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.request.user.pk
        print(pk)
        current_user = UserProfile.objects.filter(user_id=pk).get()
        context['profile'] = current_user
        return context
