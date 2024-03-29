# Generated by Django 3.2 on 2023-06-24 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0006_auto_20230624_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_authors', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='text',
            field=models.TextField(help_text='Введите отзыв, поле обязательное.', verbose_name='Отзыв'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(help_text='Введите отзыв, поле обязательное.', verbose_name='Отзыв'),
        ),
    ]
