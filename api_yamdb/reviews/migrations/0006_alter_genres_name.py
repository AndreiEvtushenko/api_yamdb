# Generated by Django 3.2 on 2023-06-16 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_rename_genres_titles_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genres',
            name='name',
            field=models.CharField(help_text='Введите название жанра, это поле обязательное', max_length=256, verbose_name='Название жанра'),
        ),
    ]
