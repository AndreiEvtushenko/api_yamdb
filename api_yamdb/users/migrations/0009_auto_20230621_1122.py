# Generated by Django 3.2 on 2023-06-21 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20230621_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(help_text='Введите имя пользователя', max_length=150, verbose_name='Имя пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, help_text='Введите фамилию пользователя', max_length=150, verbose_name='Фамилия пользователя'),
        ),
    ]
