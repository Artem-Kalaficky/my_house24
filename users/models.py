from random import randint

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from .manager import CustomUserManager


def unique_id():
    user_id = str(randint(0, 99999)).zfill(5)
    return user_id


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('E-mail', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    user_id = models.CharField(max_length=5, default=unique_id, unique=True, null=True, blank=True, verbose_name='ID')
    first_name = models.CharField(max_length=32, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=32, blank=True, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=32, blank=True, verbose_name='Отчество')
    avatar = models.ImageField(upload_to='gallery/', null=True, blank=True, verbose_name='Аватар')
    telephone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Телефон')
    viber = models.CharField(max_length=20, null=True, blank=True, verbose_name='Вайбер')
    telegram = models.CharField(max_length=20, null=True, blank=True, verbose_name='Телеграм')
    notes = models.TextField(null=True, blank=True, verbose_name='О владельце (заметки)')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    CHOICES = (('is_active', 'Активен'),
               ('new', 'Новый'),
               ('disable', 'Отключен'))
    status = models.CharField(max_length=16, choices=CHOICES, default='new', null=True, blank=True,
                              verbose_name='Статус')
    role = models.ForeignKey('Role', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Роль')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.email


class Role(models.Model):
    CHOICES = (('director', 'Директор'),
               ('manager', 'Менеджер'),
               ('accountant', 'Бухгалтер'),
               ('electric', 'Электрик'),
               ('plumber', 'Сантехник'))
    role = models.CharField(max_length=16, choices=CHOICES, default='director', blank=True, verbose_name='Роль')
    has_statistics = models.BooleanField(default=False, verbose_name='Доступ к статистике')
    has_cashbox = models.BooleanField(default=False, verbose_name='Доступ к кассе')
    has_invoice = models.BooleanField(default=False, verbose_name='Доступ к квитанциям')
    has_personal_account = models.BooleanField(default=False, verbose_name='Доступ к лицевым счетам')
    has_apartment = models.BooleanField(default=False, verbose_name='Доступ к квартирам')
    has_owner = models.BooleanField(default=False, verbose_name='Доступ к владельцам квартир')
    has_house = models.BooleanField(default=False, verbose_name='Доступ к домам')
    has_message = models.BooleanField(default=False, verbose_name='Доступ к сообщениям')
    has_application = models.BooleanField(default=False, verbose_name='Доступ к заявкам вызова мастера')
    has_meter = models.BooleanField(default=False, verbose_name='Доступ к показаниям счетчиков')
    has_site_management = models.BooleanField(default=False, verbose_name='Доступ к управлению сайтом')
    has_service = models.BooleanField(default=False, verbose_name='Доступ к услугам')
    has_tariff = models.BooleanField(default=False, verbose_name='Доступ к тарифам')
    has_role = models.BooleanField(default=False, verbose_name='Доступ к ролям')
    has_users = models.BooleanField(default=False, verbose_name='Доступ к пользователям')
    has_requisites = models.BooleanField(default=False, verbose_name='Доступ к реквизитам')

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class Message(models.Model):
    users = models.ManyToManyField(UserProfile, verbose_name='Получатели')
    topic = models.CharField(max_length=128, verbose_name='Тема сообщения')
    text = models.TextField(verbose_name='Текст сообщения')
    sender = models.CharField(max_length=128, verbose_name='Отправитель')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'




