from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelformset_factory, PasswordInput, TextInput, EmailInput, Select

from users.models import Role, UserProfile


# region SYSTEM-SETTINGS form
class RoleForm(ModelForm):
    class Meta:
        model = Role
        exclude = ('role',)


RoleFormSet = modelformset_factory(Role, form=RoleForm, extra=0)


# region users page form
class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=PasswordInput(attrs={'class': 'form-control'}),
                                help_text=password_validation.password_validators_help_texts())
    password2 = forms.CharField(label='Повторить пароль', widget=PasswordInput(attrs={'class': 'form-control'}),
                                help_text='Повторите пароль')

    class Meta:
        model = UserProfile
        fields = ('email', 'last_name', 'first_name', 'telephone', 'password1', 'password2', 'role', 'status')
        widgets = {'first_name': TextInput(attrs={'class': 'form-control'}),
                   'last_name': TextInput(attrs={'class': 'form-control'}),
                   'telephone': TextInput(attrs={'class': 'form-control'}),
                   'email': EmailInput(attrs={'class': 'form-control'}),
                   'role': Select(attrs={'class': 'form-select'}),
                   'status': Select(attrs={'class': 'form-select'})}

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
        user.is_staff = True
        if commit:
            user.save()
        return user
# endregion users page form
# endregion SYSTEM-SETTINGS form
