# Generated by Django 3.2 on 2022-08-01 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20220801_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='date_created',
        ),
    ]