from django.db import models
from django.utils import timezone

from users.models import UserProfile


# region Houses
class Section(models.Model):
    name = models.CharField(max_length=16, verbose_name='Название')

    class Meta:
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'

    def __str__(self):
        return self.name


class Floor(models.Model):
    name = models.CharField(max_length=16, verbose_name='Название')

    class Meta:
        verbose_name = 'Этаж'
        verbose_name_plural = 'Этажи'

    def __str__(self):
        return self.name


class House(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название')
    address = models.CharField(max_length=128, verbose_name='Адрес')
    image_1 = models.ImageField(upload_to='gallery/', null=True, blank=True, verbose_name='Изображение 1')
    image_2 = models.ImageField(upload_to='gallery/', null=True, blank=True, verbose_name='Изображение 2')
    image_3 = models.ImageField(upload_to='gallery/', null=True, blank=True, verbose_name='Изображение 3')
    image_4 = models.ImageField(upload_to='gallery/', null=True, blank=True, verbose_name='Изображение 4')
    image_5 = models.ImageField(upload_to='gallery/', null=True, blank=True, verbose_name='Изображение 5')
    sections = models.ManyToManyField(Section, verbose_name='Секции')
    floors = models.ManyToManyField(Floor, verbose_name='Этажи')
    users = models.ManyToManyField(UserProfile, verbose_name='Пользователи')

    class Meta:
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'

    def __str__(self):
        return self.name


class Apartment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Секция')
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name='Этаж')
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, blank=True, related_name='apartment',
                              verbose_name='Владелец')
    tariff = models.ForeignKey('Tariff', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Тариф')
    number = models.IntegerField(verbose_name='Номер квартиры')
    area = models.FloatField(null=True, blank=True, verbose_name='Площадь (кв.м.)')

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'
        unique_together = ['section', 'floor', 'number']

    def __str__(self):
        return f'{self.number}'


class Application(models.Model):
    date = models.DateField(default=timezone.now, verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    description = models.TextField(verbose_name='Описание')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, verbose_name='Квартира')
    TYPES = (('any', 'Любой специалист'),
             ('electric', 'Электрик'),
             ('plumber', 'Сантехник'))
    type_master = models.CharField(max_length=16, choices=TYPES, default='any', verbose_name='Тип мастера')
    STATUSES = (('new', 'Новая'),
                ('in_progress', 'В работе'),
                ('complete', 'Выполнена'))
    status = models.CharField(max_length=16, choices=STATUSES, default='new', verbose_name='Статус')
    master = models.ForeignKey(UserProfile, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Мастер')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Message(models.Model):
    message_for_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='message_for_owner',
                                          null=True, blank=True, verbose_name='Владелец квартиры')
    topic = models.CharField(max_length=128, verbose_name='Тема сообщения')
    text = models.TextField(verbose_name='Текст сообщения')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender', verbose_name='Отправитель')
    house = models.ForeignKey(House, on_delete=models.CASCADE, null=True, blank=True, verbose_name='ЖК')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Секция')
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Этаж')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Квартира')
    is_debt = models.BooleanField(default=False, verbose_name='Владельцам с задолженностями')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.topic
# endregion Houses


# region CRM(Settings)
def meter_reading_number():
    largest = MeterReading.objects.all().order_by('number').last()
    if not largest:
        return '1'.zfill(10)
    number = int(largest.number) + 1
    return str(number).zfill(10)


class Requisites(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название компании')
    information = models.TextField(verbose_name='Информация')

    class Meta:
        verbose_name = 'Реквизит'
        verbose_name_plural = 'Реквизиты'


class Item(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название')
    CHOICES = (('income', 'Приход'),
               ('expense', 'Расход'))
    income_expense = models.CharField(max_length=16, choices=CHOICES, default='income', verbose_name='Приход/Расход')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=16, unique=True, verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='Услуга')
    show = models.BooleanField(default=True, verbose_name='Показывать в счетчиках')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name='Ед. изм.')
    currency = models.CharField(max_length=4, default='грн', blank=True, verbose_name='Валюта')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


class MeterReading(models.Model):
    number = models.BigIntegerField(default=meter_reading_number, unique=True, verbose_name='Номер показания')
    date = models.DateField(default=timezone.now, verbose_name='Дата')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, verbose_name='Квартира')
    meter = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Счетчик')
    CHOICES = (('new', 'Новое'),
               ('accounted', 'Учтено'),
               ('paid', 'Учтено и оплачено'),
               ('zero', 'Нулевое'))
    status = models.CharField(max_length=16, choices=CHOICES, default='new', verbose_name='Статус')
    expense = models.IntegerField(verbose_name='Показания счетчика')

    class Meta:
        verbose_name = 'Показание счетчика'
        verbose_name_plural = 'Показания счетчика'

    def __str__(self):
        return str(self.number).zfill(10)


class Tariff(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='Название тарифа')
    description = models.TextField(verbose_name='Описание тарифа')
    services = models.ManyToManyField(Service, through='ServiceForTariff', through_fields=('tariff', 'service'),
                                      verbose_name='Услуги')
    date_edit = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.name


class ServiceForTariff(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, blank=True, verbose_name='Тариф')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    cost_for_unit = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = 'Услуга для тарифа'
        verbose_name_plural = 'Услуги для тарифоф'
        unique_together = ['tariff', 'service']


class ServiceForInvoice(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Квитанция')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    cost_for_unit = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена за ед., грн.')
    expense = models.IntegerField(verbose_name='Расход')
    full_cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость, грн.')

    class Meta:
        verbose_name = 'Услуга для квитанции'
        verbose_name_plural = 'Услуги для квитанций'
        unique_together = ['invoice', 'service']
# endregion CRM(Settings)


# region CRM(Accounting)
def transaction_number():
    largest = Transaction.objects.all().order_by('number').last()
    if not largest:
        return '1'.zfill(10)
    number = int(largest.number) + 1
    return str(number).zfill(10)


def invoice_number():
    largest = Invoice.objects.all().order_by('number').last()
    if not largest:
        return '1'.zfill(10)
    number = int(largest.number) + 1
    return str(number).zfill(10)


def personal_account_number():
    largest = PersonalAccount.objects.all().order_by('personal_number').last()
    if not largest:
        return '1'.zfill(10)
    number = int(largest.personal_number) + 1
    return str(number).zfill(10)


class Invoice(models.Model):
    number = models.BigIntegerField(default=invoice_number, unique=True, verbose_name='Номер квитанции')
    date = models.DateField(default=timezone.now, verbose_name='Дата')
    apartment = models.ForeignKey(Apartment, on_delete=models.PROTECT, verbose_name='Квартира')
    is_held = models.BooleanField(default=True, verbose_name='Проведена')
    CHOICES = (('paid', 'Оплачена'),
               ('p_paid', 'Частично оплачена'),
               ('unpaid', 'Неоплачена'))
    status = models.CharField(max_length=16, choices=CHOICES, default='unpaid', verbose_name='Статус')
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, verbose_name='Тариф')
    date_with = models.DateField(default=timezone.now, verbose_name='Период с')
    date_before = models.DateField(default=timezone.now, verbose_name='Период до')
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True, verbose_name='Сумма')
    services = models.ManyToManyField(Service, through=ServiceForInvoice, through_fields=('invoice', 'service'),
                                      verbose_name='Услуги')

    class Meta:
        verbose_name = 'Квитанция'
        verbose_name_plural = 'Квитанции'

    def __str__(self):
        return str(self.number).zfill(10)


class Template(models.Model):
    template = models.FileField(upload_to='files/', verbose_name='Загрузить пользовательский шаблон')
    name = models.CharField(max_length=64, verbose_name='Название')
    is_default = models.BooleanField(default=False, blank=True, verbose_name='По-умолчанию')

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'

    def __str__(self):
        return self.name


class PersonalAccount(models.Model):
    personal_number = models.BigIntegerField(default=personal_account_number, unique=True,
                                             verbose_name='Номер лицевого счета')
    CHOICES = (('active', 'Активный'),
               ('inactive', 'Неактивный'))
    status = models.CharField(choices=CHOICES, max_length=16, default='active', verbose_name='Статус')
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE, null=True, related_name='personal_account',
                                     blank=True, verbose_name='Квартира')
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Остаток (грн.)')

    class Meta:
        verbose_name = 'Лицевой счет'
        verbose_name_plural = 'Лицевые счета'

    def __str__(self):
        return str(self.personal_number).zfill(10)


class Transaction(models.Model):
    number = models.BigIntegerField(default=transaction_number, unique=True, verbose_name='Номер ведомости')
    date = models.DateField(default=timezone.now, verbose_name='Дата')
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, blank=True,
                              related_name='owner', verbose_name='Владелец квартиры')
    personal_account = models.ForeignKey(PersonalAccount, on_delete=models.PROTECT, null=True, blank=True,
                                         verbose_name='Лицевой счет')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Статья')
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Сумма')
    completed = models.BooleanField(default=True, verbose_name='Проведен')
    manager = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, blank=True, related_name='manager',
                                verbose_name='Менеджер')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    is_income = models.BooleanField(default=True, verbose_name='Приходная ведомость')

    class Meta:
        verbose_name = 'Приход/Расход'
        verbose_name_plural = 'Приходные/Расходные ведомости'

    def __str__(self):
        return str(self.number).zfill(10)
# endregion CRM(Accounting)
