# Generated by Django 5.1.3 on 2024-12-07 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EZakon_app', '0004_lawyer_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawyer',
            name='com',
            field=models.IntegerField(default='0', verbose_name='Отзывы'),
        ),
    ]
