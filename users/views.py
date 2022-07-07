from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import AdminLoginForm, RegisterUserForm, OwnerLoginForm
from .models import UserProfile
from .utilities import signer


class AdminLoginView(LoginView):
    template_name = 'users/pages/login/admin_login.html'
    authentication_form = AdminLoginForm

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        url = reverse_lazy('home')
        if not self.request.user.role.has_statistics:
            url = f"/crm/system-settings/users/update/{self.request.user.id}/"
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({self.redirect_field_name: self.get_redirect_url(),
                        'site': current_site,
                        'site_key': settings.RECAPTCHA_SITE_KEY,
                        'site_name': current_site.name,
                        **(self.extra_context or {})})
        return context


class OwnerLoginView(LoginView):
    template_name = 'users/pages/login/owner_login.html'
    authentication_form = OwnerLoginForm

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return HttpResponseRedirect(reverse_lazy('cabinet'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({self.redirect_field_name: self.get_redirect_url(),
                        'site': current_site,
                        'site_key': settings.RECAPTCHA_SITE_KEY,
                        'site_name': current_site.name,
                        **(self.extra_context or {})})
        return context


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'users/logout.html'
    next_page = reverse_lazy('owner_login')


class RegisterUserView(CreateView):
    model = UserProfile
    template_name = 'users/pages/registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'users/pages/registration/register_done.html'


def user_activate(request, sign):
    try:
        email = signer.unsign(sign)
    except BadSignature:
        return render(request, 'users/pages/activate/bad_signature.html')
    user = get_object_or_404(UserProfile, email=email)
    if user.is_active:
        template = 'users/pages/activate/user_is_activated.html'
    else:
        template = 'users/pages/activate/activation_done.html'
        user.is_active = True
        user.status = 'new'
        user.save()
    return render(request, template)


