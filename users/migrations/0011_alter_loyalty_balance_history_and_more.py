# Generated by Django 4.2 on 2024-10-10 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_customuser_birth_date_alter_customuser_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loyalty',
            name='balance_history',
            field=models.TextField(blank=True, default='\nРегистрация в системе лояльности 2024-10-10', help_text='В данном тексте будет автоматически сохраняться история выбора выгод пользователя', verbose_name='(Тех)Статистика бонусного счета'),
        ),
        migrations.AlterField(
            model_name='loyalty',
            name='benefits_history',
            field=models.TextField(blank=True, default='\nРегистрация в системе лояльности 2024-10-10', help_text='В данном тексте будет автоматически сохраняться история выбора выгод пользователя, и получение бонусов за приглашение нового пользователя.', verbose_name='(Тех)История выбора выгод счета'),
        ),
    ]
