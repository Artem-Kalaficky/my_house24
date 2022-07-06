from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import PasswordInput, TextInput, EmailInput

from .apps import user_registered
from .models import UserProfile


class AdminLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AdminLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    remember_me = forms.BooleanField(required=False)


class OwnerLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(OwnerLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    remember_me = forms.BooleanField(required=False)


class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=PasswordInput(attrs={'class': 'form-control'}),
                                help_text=password_validation.password_validators_help_texts())
    password2 = forms.CharField(label='Повторить пароль', widget=PasswordInput(attrs={'class': 'form-control'}),
                                help_text='Повторите пароль')

    class Meta:
        model = UserProfile
        fields = ('email', 'last_name', 'first_name', 'patronymic', 'password1', 'password2')
        widgets = {'first_name': TextInput(attrs={'class': 'form-control'}),
                   'last_name': TextInput(attrs={'class': 'form-control'}),
                   'patronymic': TextInput(attrs={'class': 'form-control'}),
                   'email': EmailInput(attrs={'class': 'form-control'})}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.status = 'disable'
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user
