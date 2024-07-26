# Generated by Django 4.2 on 2024-07-25 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Istok_app', '0012_description_image_projectimage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectimage',
            name='name',
        ),
        migrations.AddField(
            model_name='projectimage',
            name='image_medium',
            field=models.ImageField(blank=True, default=None, upload_to='', verbose_name='Оригинальное изображение'),
        ),
        migrations.AddField(
            model_name='projectimage',
            name='image_small',
            field=models.ImageField(blank=True, default=None, upload_to='', verbose_name='Оригинальное изображение'),
        ),
        migrations.AlterField(
            model_name='furniture',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='projectimage',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='Оригинальное изображение'),
        ),
    ]
