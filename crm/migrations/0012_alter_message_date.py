# Generated by Django 3.2 on 2022-08-03 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_auto_20220803_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата'),
        ),
    ]
