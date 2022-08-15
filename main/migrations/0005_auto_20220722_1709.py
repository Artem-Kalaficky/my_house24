# Generated by Django 3.2 on 2022-07-22 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20220718_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutservice',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание услуги'),
        ),
        migrations.AlterField(
            model_name='aboutservice',
            name='image',
            field=models.ImageField(blank=True, upload_to='gallery/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='aboutservice',
            name='name',
            field=models.CharField(blank=True, max_length=64, verbose_name='Название услуги'),
        ),
    ]