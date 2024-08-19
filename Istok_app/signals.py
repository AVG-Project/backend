from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from users.models import Profile, Loyalty
# from .models import Order, Application
from django.core.exceptions import ObjectDoesNotExist


# @receiver(post_save, sender=Orders)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         try:
#             code = instance.order_by_loyalty_code.loyalty_code
#         except Exception:
#             code = ''
#
#         if code:
#             order_user = instance.order_user
#             orders_quantity = len(Orders.objects.filter(order_user=order_user))
#             loyalty = Loyalty.objects.filter(loyalty_code=code).first()
#             if orders_quantity == 1 and loyalty:
#                 if order_user != loyalty.user:
#                     loyalty.increase_balance(instance.order_price)

# @receiver(post_save, sender=Application)
# def send_application_email(sender, instance, created, **kwargs):
#     if created:
#         subject = 'Новая заявка'
#         message = f'''
#         New application details:
#         Тип мебели: {instance.type}
#         Форма мебели: {instance.form}
#         Дополнения: {instance.addition}
#         Материал фасада: {instance.facades_material}
#         Материал столешницы: {instance.table_material}
#         Кухонная сантехника: {instance.plumb}
#         Бытовая техника: {instance.appliances}
#         Бюджет проекта: {instance.budget}
#         Консультация с экспертом по обустройству дома: {instance.consultation}
#         Фамилия: {instance.last_name}
#         Имя: {instance.first_name}
#         Отчество: {instance.patronymic}
#         Ваш номер телефона: {instance.phone}
#         Как с Вами связаться?: {instance.connection}
#         Ваша ссылка на Telegram/ВКонтакте: {instance.link}
#         Дата: {instance.data}
#         Время: {instance.time}
#         '''
#         send_mail(subject, message, 'myrsin.s@yandex.com', ['eminence_grise@inbox.ru'])
