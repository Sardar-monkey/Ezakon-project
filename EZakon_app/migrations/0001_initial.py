# Generated by Django 5.1.3 on 2024-12-07 15:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='lawyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название страшности')),
                ('description', models.TextField(default='Описание отсутствует', verbose_name='Описание страшности')),
                ('status', models.CharField(default='Нету статуса', max_length=255, verbose_name='Статус юриста')),
                ('closed', models.IntegerField(default='0', verbose_name='Дел закрыто')),
                ('succses', models.CharField(default='0 успешных', max_length=50, verbose_name='Успешно закрыто')),
                ('stazh', models.IntegerField(default='0', verbose_name='Стаж работы')),
                ('phone', models.IntegerField(max_length=255, verbose_name='номер телефона')),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='Время создания')),
            ],
            options={
                'verbose_name': 'Страшность',
                'verbose_name_plural': 'Страшности',
            },
        ),
    ]