# Generated by Django 3.2 on 2023-06-16 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20230616_1107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='titles',
            old_name='genre',
            new_name='genres',
        ),
        migrations.AlterField(
            model_name='categories',
            name='name',
            field=models.CharField(help_text='Введите название категории, это поле обязательное', max_length=256, unique=True, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='genres',
            name='name',
            field=models.CharField(help_text='Введите название жанра, это поле обязательное', max_length=256, unique=True, verbose_name='Название жанра'),
        ),
    ]
