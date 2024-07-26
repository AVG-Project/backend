# Generated by Django 4.2 on 2024-07-25 08:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Istok_app', '0011_remove_furniturecolors_color_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_number', models.PositiveIntegerField(verbose_name='Порядковый номер части текста')),
                ('text', models.TextField(default='Нет описание мебели', verbose_name='Описание мебели')),
            ],
            options={
                'verbose_name': 'Текст',
                'verbose_name_plural': 'Тексты',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Медиа файлы',
            },
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
        ),
        migrations.AddField(
            model_name='furniture',
            name='time_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 25, 8, 40, 32, 165332, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='furniture',
            name='tags',
            field=models.ManyToManyField(related_name='tags', through='Istok_app.FurnitureTags', to='Istok_app.tags', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='furniture',
            name='text',
            field=models.TextField(verbose_name='Описание мебели'),
        ),
    ]
