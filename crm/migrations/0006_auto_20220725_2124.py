# Generated by Django 3.2 on 2022-07-25 18:24

import crm.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_alter_servicefortariff_tariff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalaccount',
            name='number',
            field=models.BigIntegerField(blank=True, default=crm.models.personal_account_number, unique=True, verbose_name='Номер лицевого счета'),
        ),
        migrations.AlterUniqueTogether(
            name='apartment',
            unique_together={('section', 'floor', 'number')},
        ),
    ]