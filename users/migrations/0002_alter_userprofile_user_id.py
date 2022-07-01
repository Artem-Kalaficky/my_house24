# Generated by Django 3.2 on 2022-07-01 13:34

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_id',
            field=models.IntegerField(blank=True, default=users.models.unique_id, null=True, unique=True, verbose_name='ID'),
        ),
    ]
