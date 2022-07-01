from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms import AdminLoginForm


class AdminLoginView(LoginView):
    template_name = 'users/admin_login.html'
    authentication_form = AdminLoginForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(reverse_lazy('home'))


class OwnerLoginView(LoginView):
    template_name = 'users/owner_login.html'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(reverse_lazy('cabinet'))

