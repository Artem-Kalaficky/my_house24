# Generated by Django 3.2 on 2022-07-16 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_role_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='remember_me',
        ),
    ]