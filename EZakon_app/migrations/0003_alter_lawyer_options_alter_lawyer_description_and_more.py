# Generated by Django 5.1.3 on 2024-12-07 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EZakon_app', '0002_lawyer_image_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lawyer',
            options={'verbose_name': 'Резюме юриста', 'verbose_name_plural': 'Резюме юристов'},
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='description',
            field=models.TextField(default='Описание отсутствует', verbose_name='Описание юриста'),
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Имя юриста'),
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='succses',
            field=models.IntegerField(default=0, verbose_name='Успешно закрыто дел'),
        ),
    ]