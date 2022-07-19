from django import forms
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm, modelformset_factory, TextInput, Select, Textarea, NumberInput, URLInput, EmailInput

from main.models import MainPage, Seo, Block, AboutPage, Photo, Document, ServicePage, AboutService, ContactPage
from users.models import Role
from .models import Item, Requisites, Service, Unit, Tariff, ServiceForTariff


# region SITE-MANAGEMENT
# region Main Page
class SeoForm(ModelForm):
    class Meta:
        model = Seo
        fields = ('title', 'description', 'keywords')
        widgets = {'title': TextInput(attrs={'class': 'form-control'}),
                   'description': Textarea(attrs={'rows': 5,
                                                  'class': 'form-control'}),
                   'keywords': Textarea(attrs={'rows': 5,
                                               'class': 'form-control'})}


class MainPageForm(ModelForm):
    def clean_slide_1(self):
        picture = self.cleaned_data.get("slide_1")
        w, h = get_image_dimensions(picture)
        if w != 1920 and h != 800:
            raise forms.ValidationError("Размеры слайда не валидны")
        return picture

    def clean_slide_2(self):
        picture = self.cleaned_data.get("slide_2")
        w, h = get_image_dimensions(picture)
        if w != 1920 and h != 800:
            raise forms.ValidationError("Размеры слайда не валидны")
        return picture

    def clean_slide_3(self):
        picture = self.cleaned_data.get("slide_3")
        w, h = get_image_dimensions(picture)
        if w != 1920 and h != 800:
            raise forms.ValidationError("Размеры слайда не валидны")
        return picture

    class Meta:
        model = MainPage
        fields = ('slide_1', 'slide_2', 'slide_3', 'header', 'text', 'show_urls')
        widgets = {'header': TextInput(attrs={'class': 'form-control'}),
                   'text': Textarea(attrs={'rows': 5,
                                           'class': 'form-control'})}


class BlockForm(ModelForm):
    def clean_image(self):
        picture = self.cleaned_data.get("image")
        w, h = get_image_dimensions(picture)
        if w != 1000 and h != 600:
            raise forms.ValidationError("Размеры слайда не валидны")
        return picture

    class Meta:
        model = Block
        fields = ('image', 'header', 'description')
        widgets = {'header': TextInput(attrs={'class': 'form-control'}),
                   'description': Textarea(attrs={'rows': 5,
                                                  'class': 'form-control'})}


BlockFormSet = modelformset_factory(Block, form=BlockForm, extra=0, can_delete=True)
# endregion Main Page


# region About Page
class AboutPageForm(ModelForm):
    def clean_avatar(self):
        picture = self.cleaned_data.get("avatar")
        w, h = get_image_dimensions(picture)
        if w != 250 and h != 310:
            raise forms.ValidationError("Размеры картинки не валидны")
        return picture

    class Meta:
        model = AboutPage
        fields = ('header', 'text', 'avatar', 'additional_header', 'additional_text')
        widgets = {'header': TextInput(attrs={'class': 'form-control'}),
                   'text': Textarea(attrs={'rows': 5,
                                           'class': 'form-control'}),
                   'additional_header': TextInput(attrs={'class': 'form-control'}),
                   'additional_text': Textarea(attrs={'rows': 5,
                                                      'class': 'form-control'})}


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ('photo', 'is_main')


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'document')
        widgets = {'name': TextInput(attrs={'class': 'form-control'})}


DocumentFormSet = modelformset_factory(Document, form=DocumentForm, extra=0, can_delete=True)
# endregion About Page


# region Services Page
class ServicePageForm(ModelForm):
    class Meta:
        model = ServicePage
        fields = ()


class AboutServiceForm(ModelForm):
    class Meta:
        model = AboutService
        fields = ('image', 'name', 'description')
        widgets = {'name': TextInput(attrs={'class': 'form-control'}),
                   'description': Textarea(attrs={'rows': 6,
                                                  'class': 'form-control'})}


AboutServiceFormSet = modelformset_factory(AboutService, form=AboutServiceForm, extra=0, can_delete=True)
# endregion Services Page


# region Contact Page
class ContactPageForm(ModelForm):
    class Meta:
        model = ContactPage
        fields = ('header', 'text', 'url', 'full_name', 'location', 'address', 'telephone', 'email', 'map')
        widgets = {'header': TextInput(attrs={'class': 'form-control'}),
                   'text': Textarea(attrs={'rows': 5,
                                           'class': 'form-control'}),
                   'url': URLInput(attrs={'class': 'form-control'}),
                   'full_name': TextInput(attrs={'class': 'form-control'}),
                   'location': TextInput(attrs={'class': 'form-control'}),
                   'address': TextInput(attrs={'class': 'form-control'}),
                   'telephone': TextInput(attrs={'class': 'form-control'}),
                   'email': EmailInput(attrs={'class': 'form-control'}),
                   'map': Textarea(attrs={'rows': 5,
                                          'class': 'form-control'})}
# endregion Contact Page
# endregion SITE-MANAGEMENT


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
