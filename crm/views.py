from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import RoleFormSet, ItemForm, RequisiteForm, ServiceFormSet, UnitFormSet, ServiceForTariffFormSet, \
    TariffForm
from users.forms import UserCreateForm, ChangeUserInfoForm
from users.models import UserProfile, Role
from .models import Item, Requisites, Service, Unit, Tariff, ServiceForTariff


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/admin/login/'

    def test_func(self):
        return self.request.user.is_staff


class StatisticsTemplateView(StaffRequiredMixin, TemplateView):
    template_name = 'crm/pages/statistics.html'


# region SYSTEM-SETTINGS
# region services page
class ServiceCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/system_settings/services.html'
    success_message = 'Услуги успешно отредактированны!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = Service.objects.select_related('unit')
        idx = []
        for service in services:
            idx.append(service.unit.id)
        context['idx'] = idx
        context['unit_formset'] = UnitFormSet(self.request.POST or None, queryset=Unit.objects.all(),
                                              prefix='unit_formset')
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = ServiceFormSet(self.request.POST or None, queryset=Service.objects.all())
        return form_class

    def form_valid(self, form):
        unit_formset = self.get_context_data()['unit_formset']
        unit_formset.save(commit=False)
        for unit in unit_formset.deleted_objects:
            unit.delete()
        for unit in unit_formset:
            if unit.is_valid() and unit.cleaned_data:
                unit.save()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('services')
# endregion services page


# region tariffs page
class TariffsListView(StaffRequiredMixin, SuccessMessageMixin, ListView):
    template_name = 'crm/pages/system_settings/tariffs/tariffs_list.html'
    context_object_name = 'tariffs'

    def get_queryset(self):
        queryset = Tariff.objects.all()
        if self.request.GET.get('filter') == '1':
            queryset = queryset.order_by('name')
        if self.request.GET.get('filter') == '0':
            queryset = queryset.order_by('-name')
        return queryset


class TariffDetailView(StaffRequiredMixin, DetailView):
    queryset = Tariff.objects.prefetch_related('servicefortariff_set__service__unit')
    template_name = 'crm/pages/system_settings/tariffs/tariff_detail.html'


class TariffCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/system_settings/tariffs/tariff_create.html'
    success_message = 'Тариф успешно создан!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = ServiceForTariffFormSet(self.request.POST or None,
                                                     queryset=ServiceForTariff.objects.none(), prefix='formset')
        context['units'] = Unit.objects.all()
        context['services'] = Service.objects.select_related('unit')
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = TariffForm(self.request.POST or None)
        return form_class

    def form_valid(self, form):
        form.save()
        formset = self.get_context_data()['formset']
        for obj in formset:
            if obj.is_valid():
                serv_for_tar = obj.save(commit=False)
                if obj.cleaned_data:
                    serv_for_tar.tariff = form.instance
                    serv_for_tar.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tariffs_list')


class TariffUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tariff
    template_name = 'crm/pages/system_settings/tariffs/tariff_update.html'
    success_url = reverse_lazy('tariffs_list')
    success_message = 'Данные о тарифе обновлены!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = ServiceForTariffFormSet(self.request.POST or None,
                                                     queryset=ServiceForTariff.objects.filter(tariff_id=self.object.id),
                                                     prefix='formset')
        context['services'] = Service.objects.select_related('unit')
        context['units'] = Unit.objects.all()
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = TariffForm(self.request.POST or None, instance=self.object)
        return form_class

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        form.save()
        formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for obj in formset:
            if obj.is_valid() and obj.cleaned_data:
                obj.instance.tariff = form.instance
                obj.save()
        return super().form_valid(form)


class TariffDeleteView(SuccessMessageMixin, DeleteView):
    model = Tariff
    success_url = reverse_lazy('tariffs_list')
    success_message = 'Тариф успешно удалён!'
# endregion tariffs page


# region roles page
class RoleCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/system_settings/roles.html'
    success_message = 'Роли успешно изменены!'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = RoleFormSet(self.request.POST or None, queryset=Role.objects.all())
        return form_class

    def get_success_url(self):
        return reverse('roles')
# endregion roles page


# region users page
class UsersListView(StaffRequiredMixin, ListView):
    template_name = 'crm/pages/system_settings/users/users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = UserProfile.objects.filter(is_staff=True).select_related('role').order_by('pk')
        if self.request.GET.get('user'):
            queryset = queryset.filter(Q(last_name__icontains=self.request.GET.get('user')) |
                                       Q(first_name__icontains=self.request.GET.get('user')))
        if self.request.GET.get('role'):
            queryset = queryset.filter(role__role=self.request.GET.get('role'))
        if self.request.GET.get('telephone'):
            queryset = queryset.filter(telephone__icontains=self.request.GET.get('telephone'))
        if self.request.GET.get('email'):
            queryset = queryset.filter(email__icontains=self.request.GET.get('email'))
        if self.request.GET.get('status'):
            queryset = queryset.filter(status=self.request.GET.get('status'))
        return queryset


class UserCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/system_settings/users/user_create.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно создан!'


class UserDetailView(StaffRequiredMixin, DetailView):
    queryset = UserProfile.objects.select_related('role')
    template_name = 'crm/pages/system_settings/users/user_detail.html'


class UserUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ChangeUserInfoForm
    queryset = UserProfile.objects.select_related('role')
    template_name = 'crm/pages/system_settings/users/user_update.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Данные о пользователе обновлены!'


class UserDeleteView(SuccessMessageMixin, DeleteView):
    model = UserProfile
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно удалён!'
# endregion users page


# region requisites
class RequisiteUpdate(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = RequisiteForm
    model = Requisites
    template_name = 'crm/pages/system_settings/requisites.html'
    success_url = reverse_lazy('requisites', kwargs={'pk': 1})
    success_message = 'Реквизиты обновлены!'
# endregion requisites


# region items page
class ItemsListView(StaffRequiredMixin, ListView):
    template_name = 'crm/pages/system_settings/items/items_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = Item.objects.all()
        if self.request.GET.get('filter') == '0':
            queryset = queryset.order_by('income_expense')
        if self.request.GET.get('filter') == '1':
            queryset = queryset.order_by('-income_expense')
        return queryset


class ItemCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/system_settings/items/item_create.html'
    form_class = ItemForm
    success_url = reverse_lazy('items_list')
    success_message = 'Статья успешно добавлена!'


class ItemUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'crm/pages/system_settings/items/item_update.html'
    success_url = reverse_lazy('items_list')
    success_message = 'Данные о статье успешно обновлены!'


class ItemDeleteView(SuccessMessageMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('items_list')
    success_message = 'Статья успешно удалёна!'
# endregion items page
# endregion SYSTEM-SETTINGS
