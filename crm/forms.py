from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm, modelformset_factory, TextInput, Select, Textarea, NumberInput, URLInput, \
    EmailInput, formset_factory, PasswordInput

from main.models import MainPage, Seo, Block, AboutPage, Photo, Document, ServicePage, AboutService, ContactPage
from users.models import Role, UserProfile
from users.tasks import send_change_password_notification
from .models import Item, Requisites, Service, Unit, Tariff, ServiceForTariff, House, Section, Floor


class DateInputWidget(forms.DateInput):
    input_type = 'date'

    def format_value(self, value):
        return value


# region Owners
class OwnerCreateForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=PasswordInput(attrs={'class': 'form-control'}),
                                help_text=password_validation.password_validators_help_texts())
    password2 = forms.CharField(label='Повторить пароль', widget=PasswordInput(attrs={'class': 'form-control'}),
                                help_text='Повторите пароль')

    class Meta:
        model = UserProfile
        fields = ('avatar', 'first_name', 'last_name', 'patronymic', 'birth_date', 'telephone', 'viber', 'telegram',
                  'email', 'status', 'user_id', 'notes', 'password1', 'password2')
        widgets = {'first_name': TextInput(attrs={'class': 'form-control'}),
                   'last_name': TextInput(attrs={'class': 'form-control'}),
                   'patronymic': TextInput(attrs={'class': 'form-control'}),
                   'email': EmailInput(attrs={'class': 'form-control'}),
                   'birth_date': DateInputWidget(attrs={'type': 'date',
                                                        'class': 'form-control',
                                                        'min': '1920-01-01',
                                                        'max': '2008-01-01'}),

                   'telephone': TextInput(attrs={'class': 'form-control'}),
                   'viber': TextInput(attrs={'class': 'form-control'}),
                   'telegram': TextInput(attrs={'class': 'form-control'}),
                   'status': Select(attrs={'class': 'form-select'}),
                   'user_id': TextInput(attrs={'class': 'form-control'}),
                   'notes': Textarea(attrs={'rows': 10,
                                            'class': 'form-control'})}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.status = 'new'
        if commit:
            user.save()
        return user


class OwnerUpdateForm(UserChangeForm):
    error_messages = {"password_mismatch": "Введённые пароли не совпадают."}
    password1 = forms.CharField(required=False, label='Пароль', widget=PasswordInput(attrs={'class': 'form-control'}),
                                help_text=password_validation.password_validators_help_texts())
    password2 = forms.CharField(required=False, label='Повторить пароль', widget=PasswordInput(attrs={'class': 'form-control'}),
                                help_text='Повторите пароль')

    class Meta:
        model = UserProfile
        fields = ('avatar', 'first_name', 'last_name', 'patronymic', 'birth_date', 'telephone', 'viber', 'telegram',
                  'email', 'status', 'user_id', 'notes', 'password1', 'password2')
        widgets = {'first_name': TextInput(attrs={'class': 'form-control'}),
                   'last_name': TextInput(attrs={'class': 'form-control'}),
                   'patronymic': TextInput(attrs={'class': 'form-control'}),
                   'email': EmailInput(attrs={'class': 'form-control'}),
                   'birth_date': DateInputWidget(attrs={'type': 'date',
                                                        'class': 'form-control',
                                                        'min': '1920-01-01',
                                                        'max': '2008-01-01'}),

                   'telephone': TextInput(attrs={'class': 'form-control'}),
                   'viber': TextInput(attrs={'class': 'form-control'}),
                   'telegram': TextInput(attrs={'class': 'form-control'}),
                   'status': Select(attrs={'class': 'form-select'}),
                   'user_id': TextInput(attrs={'class': 'form-control'}),
                   'notes': Textarea(attrs={'rows': 10,
                                            'class': 'form-control'})}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not password1 and not password2:
            pass
        else:
            if password1 and password2 and password1 != password2:
                raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
            return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        if not self.cleaned_data['password1']:
            if commit:
                user.save()
            return user
        else:
            user.set_password(self.cleaned_data['password1'])
            if commit:
                user.save()
            send_change_password_notification.delay(user.email)
            return user


class InviteForm(forms.Form):
    telephone = forms.CharField(required=False, label='Телефон',
                                widget=TextInput(attrs={'class': 'form-control',
                                                        'placeholder': '+380(099) 999-99-99'}))
    email = forms.CharField(label='E-mail', widget=EmailInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'email@example.com'}))
# endregion Owners


# region Houses
class HouseForm(ModelForm):
    def clean_image_1(self):
        if self.cleaned_data.get("image_1"):
            picture = self.cleaned_data.get("image_1")
            w, h = get_image_dimensions(picture)
            if w != 522 and h != 350:
                raise forms.ValidationError("Размеры изображения не валидны")
            return picture

    def clean_image_2(self):
        if self.cleaned_data.get("image_2"):
            picture = self.cleaned_data.get("image_2")
            w, h = get_image_dimensions(picture)
            if w != 248 and h != 160:
                raise forms.ValidationError("Размеры изображения не валидны")
            return picture

    def clean_image_3(self):
        if self.cleaned_data.get("image_3"):
            picture = self.cleaned_data.get("image_3")
            w, h = get_image_dimensions(picture)
            if w != 248 and h != 160:
                raise forms.ValidationError("Размеры изображения не валидны")
            return picture

    def clean_image_4(self):
        if self.cleaned_data.get("image_4"):
            picture = self.cleaned_data.get("image_4")
            w, h = get_image_dimensions(picture)
            if w != 248 and h != 160:
                raise forms.ValidationError("Размеры изображения не валидны")
            return picture

    def clean_image_5(self):
        if self.cleaned_data.get("image_5"):
            picture = self.cleaned_data.get("image_5")
            w, h = get_image_dimensions(picture)
            if w != 248 and h != 160:
                raise forms.ValidationError("Размеры изображения не валидны")
            return picture

    class Meta:
        model = House
        fields = ('name', 'address', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5')
        widgets = {'name': TextInput(attrs={'class': 'form-control'}),
                   'address': TextInput(attrs={'class': 'form-control'})}


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ('name',)
        widgets = {'name': TextInput(attrs={'class': 'form-control'})}


class FloorForm(ModelForm):
    class Meta:
        model = Floor
        fields = ('name',)
        widgets = {'name': TextInput(attrs={'class': 'form-control'})}


class UserForm(forms.Form):
    user = forms.ModelChoiceField(required=False, label='ФИО',
                                  queryset=UserProfile.objects.filter(is_staff=True),
                                  widget=Select(attrs={'class': 'form-select',
                                                       'onchange': 'select_user(this.id)'}))
    role = forms.CharField(label='Роль', widget=TextInput(attrs={'class': 'form-control',
                                                                 'readonly': 'true'}))


SectionFormSet = modelformset_factory(Section, form=SectionForm, extra=0, can_delete=True)
FloorFormSet = modelformset_factory(Floor, form=FloorForm, extra=0, can_delete=True)
UserFormSet = formset_factory(form=UserForm, extra=0, can_delete=True)
# endregion Houses


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
