import datetime

from django.db import models

from users.models import UserProfile


# region CRM(Settings)
class Unit(models.Model):
    name = models.CharField(max_length=16, verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'
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
    largest = PersonalAccount.objects.all().order_by('number').last()
    if not largest:
        return '1'.zfill(10)
    number = int(largest.number) + 1
    return str(number).zfill(10)


class Invoice(models.Model):
    number = models.BigIntegerField(default=invoice_number, unique=True, verbose_name='Номер квитанции')
    date = models.DateField(default=datetime.date.today(), verbose_name='Дата')
    apartment = models.ForeignKey('Apartment', on_delete=models.PROTECT, verbose_name='Квартира')
    is_held = models.BooleanField(default=True, verbose_name='Проведена')
    CHOICES = ((None, 'Выберите...'),
               ('paid', 'Оплачена'),
               ('p_paid', 'Частично оплачена'),
               ('unpaid', 'Неоплачена'))
    status = models.CharField(max_length=16, choices=CHOICES, default='paid', verbose_name='Статус')
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, verbose_name='Тариф')
    date_with = models.DateField(default=datetime.date.today(), verbose_name='Период с')
    date_before = models.DateField(default=datetime.date.today(), verbose_name='Период до')
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Сумма')
    services = models.ManyToManyField(Service, through=ServiceForInvoice, through_fields=('invoice', 'service'), verbose_name='Услуги')

    class Meta:
        verbose_name = 'Квитанция'
        verbose_name_plural = 'Квитанции'


class PersonalAccount(models.Model):
    number = models.BigIntegerField(default=personal_account_number, unique=True, verbose_name='Номер лицевого счета')
    CHOICES = (('active', 'Активный'),
               ('inactive', 'Неактивный'))
    status = models.CharField(choices=CHOICES, max_length=16, default='active', verbose_name='Статус')
    apartment = models.ForeignKey('Apartment', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Квартира')
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Остаток (грн.)')

    class Meta:
        verbose_name = 'Лицевой счет'
        verbose_name_plural = 'Лицевые счета'


class Transaction(models.Model):
    number = models.BigIntegerField(default=transaction_number, unique=True, verbose_name='Номер ведомости')
    date = models.DateField(default=datetime.date.today(), verbose_name='Дата')
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Владелец квартиры')
    personal_account = models.ForeignKey(PersonalAccount, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Лицевой счет')
    item = models.ForeignKey('Item', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Статья')
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Сумма')
    completed = models.BooleanField(default=True, verbose_name='Проведен')
    manager = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Менеджер')
    comment = models.TextField(verbose_name='Комментарий')
    is_income = models.BooleanField(default=True, verbose_name='Приходная ведомость')

    class Meta:
        verbose_name = 'Приход/Расход'
        verbose_name_plural = 'Приходные/Расходные ведомости'
# endregion CRM(Accounting)


# region Houses
class Section(models.Model):
    name = models.CharField(max_length=16, verbose_name='Название')

    class Meta:
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'


class Floor(models.Model):
    name = models.CharField(max_length=16, verbose_name='Название')

    class Meta:
        verbose_name = 'Этаж'
        verbose_name_plural = 'Этажи'


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


class Apartment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Секция')
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name='Этаж')
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Владелец')
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Тариф')
    number = models.IntegerField(verbose_name='Номер квартиры')
    area = models.FloatField(null=True, blank=True, verbose_name='Площадь (кв.м.)')
    personal_account = models.OneToOneField(PersonalAccount, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Лицевой счет')

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'
        unique_together = ['floor', 'number']
# endregion Houses






