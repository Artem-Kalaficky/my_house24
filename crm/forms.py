from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelformset_factory, PasswordInput, TextInput, EmailInput, Select, Textarea

from users.models import Role
from .models import Item, Requisites, Service, Unit


# region SYSTEM-SETTINGS form
# region services
class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'show', 'unit')
        widgets = {'name': TextInput(attrs={'class': 'form-control'}),
                   'unit': Select(attrs={'class': 'form-select'})}


ServiceFormSet = modelformset_factory(Service, form=ServiceForm, extra=0, can_delete=True)


class UnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = ('name',)
        widgets = {'name': TextInput(attrs={'class': 'form-control'})}


UnitFormSet = modelformset_factory(Unit, form=UnitForm, extra=0, can_delete=True)
# endregion services


class RoleForm(ModelForm):
    class Meta:
        model = Role
        exclude = ('role',)


RoleFormSet = modelformset_factory(Role, form=RoleForm, extra=0)


class RequisiteForm(ModelForm):
    class Meta:
        model = Requisites
        fields = ('name', 'information')
        widgets = {'name': TextInput(attrs={'class': 'form-control'}),
                   'information': Textarea(attrs={'rows': 3,
                                                  'class': 'form-control'})}


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'income_expense')
        widgets = {'name': TextInput(attrs={'class': 'form-control'}),
                   'income_expense': Select(attrs={'class': 'form-select'})}
# endregion SYSTEM-SETTINGS form
