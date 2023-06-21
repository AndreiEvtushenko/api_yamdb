# Generated by Django 3.2 on 2023-06-21 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('user', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='user', help_text='Можно выбрать из трех: "user" "moderator" "admin"', max_length=50, verbose_name='Модель пользователя'),
        ),
    ]
