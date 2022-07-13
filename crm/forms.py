from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelformset_factory, PasswordInput, TextInput, EmailInput, Select, Textarea, \
    NumberInput

from users.models import Role
from .models import Item, Requisites, Service, Unit, Tariff, ServiceForTariff


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


# region tariffs
class TariffForm(ModelForm):
    class Meta:
        model = Tariff
        fields = ('name', 'description')
        widgets = {'name': TextInput(attrs={'class': 'form-control'}),
                   'description': Textarea(attrs={'rows': 3,
                                                  'class': 'form-control'})}


class ServiceForTariffForm(ModelForm):
    units = forms.ModelChoiceField(required=False, label='Ед. изм.', queryset=Unit.objects.select_related(),
                                   widget=Select(attrs={'class': 'form-select',
                                                        'disabled': 'true'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.fields['units'].initial = kwargs.get('instance').service.unit.id

    class Meta:
        model = ServiceForTariff
        fields = ('service', 'tariff', 'cost_for_unit')
        widgets = {'service': Select(attrs={'class': 'form-select'}),
                   'cost_for_unit': NumberInput(attrs={'class': 'form-control'})}


ServiceForTariffFormSet = modelformset_factory(ServiceForTariff, form=ServiceForTariffForm, extra=0, can_delete=True)
# endregion tariffs


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
