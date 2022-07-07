from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, FormView, DetailView
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView

from .forms import RoleFormSet, ItemForm
from users.forms import UserCreateForm, ChangeUserInfoForm
from users.models import UserProfile, Role
from .models import Item


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/admin/login/'

    def test_func(self):
        return self.request.user.is_staff


class StatisticsTemplateView(StaffRequiredMixin, TemplateView):
    template_name = 'crm/pages/statistics.html'


# region SYSTEM-SETTINGS
class RoleCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'crm/pages/system_settings/roles.html'
    success_message = 'Роли успешно изменены!'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = RoleFormSet(self.request.POST or None, queryset=Role.objects.all())
        return form_class

    def get_success_url(self):
        return reverse('roles')


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


# region items page
class ItemsListView(StaffRequiredMixin, ListView):
    model = Item
    template_name = 'crm/pages/system_settings/items/items_list.html'
    context_object_name = 'items'


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
