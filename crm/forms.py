from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelformset_factory, PasswordInput, TextInput, EmailInput, Select

from users.models import Role
from .models import Item


# region SYSTEM-SETTINGS form
class RoleForm(ModelForm):
    class Meta:
        model = Role
        exclude = ('role',)


RoleFormSet = modelformset_factory(Role, form=RoleForm, extra=0)


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'income_expense')
        widgets = {'name': TextInput(attrs={'class': 'form-control'}),
                   'income_expense': Select(attrs={'class': 'form-select'})}
# endregion SYSTEM-SETTINGS form
