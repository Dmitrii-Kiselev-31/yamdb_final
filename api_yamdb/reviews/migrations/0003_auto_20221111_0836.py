# Generated by Django 2.2.16 on 2022-11-11 08:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20221110_1742'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='comments',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='comments',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
    ]
