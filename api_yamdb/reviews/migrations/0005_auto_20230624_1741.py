# Generated by Django 3.2 on 2023-06-24 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20230624_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='name',
            field=models.CharField(help_text='Введите название категории, это поле обязательное', max_length=256, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='genres',
            name='name',
            field=models.CharField(help_text='Введите название жанра, это поле обязательное', max_length=256, verbose_name='Название жанра'),
        ),
    ]
