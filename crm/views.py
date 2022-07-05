from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.edit import FormMixin, CreateView, UpdateView

from crm.forms import RoleForm, RoleFormSet
from users.models import UserProfile, Role


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class StatisticsTemplateView(StaffRequiredMixin, TemplateView):
    template_name = 'crm/pages/statistics.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['new_users'] = UserProfile.objects.filter(status='new')
        return self.render_to_response(context)


# region System settings
class RoleFormView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/system_settings/roles.html'
    success_message = 'Роли успешно изменены!'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = RoleFormSet(self.request.POST or None, queryset=Role.objects.all())
        return form_class

    def get_context_data(self, **kwargs):
        context = super(RoleFormView, self).get_context_data(**kwargs)
        context['new_users'] = UserProfile.objects.filter(status='new')
        return context

    def get_success_url(self):
        return reverse_lazy('roles')





# endregion System settings
