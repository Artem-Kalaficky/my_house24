from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, DetailView

from crm.forms import OwnerUpdateForm
from crm.models import Apartment, House, Application, Message, Invoice
from personal_cabinet.forms import OwnerApplicationForm
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


# region Summary
class OwnerApartmentDetailView(OwnerRequiredMixin, DetailView):
    queryset = Apartment.objects.select_related('section', 'personal_account')
    template_name = 'personal_cabinet/pages/summary/apartment_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expense = Invoice.objects.aggregate(sum=Sum('amount', filter=Q(is_held=True, apartment=self.object)))['sum']
        context['expense'] = expense if expense else '0,00'
        return context
# endregion Summary


# region Invoices
class OwnerInvoicesListView(OwnerRequiredMixin, ListView):
    template_name = 'personal_cabinet/pages/invoices/invoices_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        queryset = Invoice.objects.filter(apartment_id__in=[x.id for x in self.request.user.apartment.all()])
        if self.request.GET.get('input_date'):
            queryset = queryset.filter(date=self.request.GET.get('input_date'))
        if self.request.GET.get('filter-date') == '0':
            queryset = queryset.order_by('date')
        if self.request.GET.get('filter-date') == '1':
            queryset = queryset.order_by('-date')
        if self.request.GET.get('status'):
            queryset = queryset.filter(status=self.request.GET.get('status'))
        return queryset
# endregion Invoices


# region Messages
class OwnerMessagesListView(OwnerRequiredMixin, ListView):
    model = Message
    template_name = 'personal_cabinet/pages/messages/messages_list.html'


class OwnerMessageDetailView(OwnerRequiredMixin, DetailView):
    queryset = Message.objects.select_related('sender')
    template_name = 'personal_cabinet/pages/messages/message_detail.html'


class OwnerMessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('owner_messages_list')
# endregion Messages


# region Applications
class OwnerApplicationsListView(OwnerRequiredMixin, ListView):
    template_name = 'personal_cabinet/pages/applications/applications_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        queryset = Application.objects.filter(apartment_id__in=[x.id for x in self.request.user.apartment.all()])
        return queryset


class OwnerApplicationCreateView(OwnerRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = OwnerApplicationForm
    template_name = 'personal_cabinet/pages/applications/application_create.html'
    success_url = reverse_lazy('owner_applications_list')
    success_message = 'Новая заявка успешно создана!'


class OwnerApplicationDeleteView(DeleteView):
    model = Application
    success_url = reverse_lazy('owner_applications_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
# endregion Applications


# region profile
class ProfileListView(BaseRequiredMixin, ListView):
    model = Apartment
    template_name = 'personal_cabinet/pages/profile/profile_list.html'
    context_object_name = 'apartments'


class ProfileUpdateView(UpdateRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    form_class = OwnerUpdateForm
    template_name = 'personal_cabinet/pages/profile/profile_update.html'
    success_url = reverse_lazy('owner_profile')
    success_message = 'Данные о профиле успешно обновлены!'
# endregion profile
