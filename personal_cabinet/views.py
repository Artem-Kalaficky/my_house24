from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView

from crm.forms import OwnerUpdateForm
from crm.models import Apartment, House
from users.models import UserProfile


# region permissions
class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/cabinet/login/'

    def test_func(self):
        return not self.request.user.is_staff and (len(self.request.user.apartment.all()) > 0)


class BaseRequiredMixin(OwnerRequiredMixin):
    def test_func(self):
        return not self.request.user.is_staff


class UpdateRequiredMixin(OwnerRequiredMixin):
    def test_func(self):
        return not self.request.user.is_staff and (f'/{self.request.user.id}/' in self.request.path)
# endregion permissions


# region summary
class SummaryTemplateView(OwnerRequiredMixin, TemplateView):
    template_name = 'personal_cabinet/pages/summary.html'
# endregion summary


# region profile
class ProfileListView(BaseRequiredMixin, ListView):
    model = Apartment
    template_name = 'personal_cabinet/pages/profile/profile_list.html'
    context_object_name = 'apartments'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.prefetch_related('sections').all()
        return context


class ProfileUpdateView(UpdateRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    form_class = OwnerUpdateForm
    template_name = 'personal_cabinet/pages/profile/profile_update.html'
    success_url = reverse_lazy('owner_profile')
    success_message = 'Данные о профиле успешно обновлены!'
# endregion profile
