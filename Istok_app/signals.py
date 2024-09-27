from django.core.mail import send_mail
from django.db.models.signals import post_save, m2m_changed, post_delete, pre_delete
from django.dispatch import receiver

from . import models
from users import models as user_models
from django.contrib.auth.models import User
# from .models import Order, Application
from django.db.models.signals import ModelSignal



@receiver(post_save, sender=models.Order)
def create_order(sender, instance, created, **kwargs):
    friends_code = instance.loyalty_code
    code_not_same = bool(friends_code != instance.user.loyalty.code)
    if friends_code and code_not_same:
        friends_loyalty = user_models.Loyalty.objects.filter(code=friends_code).first()
        buyer_loyalty = instance.user.loyalty

        if friends_loyalty and not instance.user.loyalty.friends_loyalty_used:
            buyer_loyalty.friends_loyalty = friends_loyalty
            buyer_loyalty.save()
            try:
                user_models.LoyaltyBenefit.objects.create(loyalty=friends_loyalty)
                text = 'Кодом пользователя воспользовались. Посылается письмо с оповещением'
                print(text)
                # todo send_email_user
            except Exception as e:
                print(e)
                #todo send_mail_admin()
        elif not friends_loyalty:
            #todo send_mail_staff
            print('В заказе был указан код лояльности, но в базе данных его нет. '
                  'Возможно при оформлении была допущена ошибка покупателем или сотрудником')
        else:
            print('Кодом путаются воспользоваться во второй раз')


@receiver(post_save, sender=user_models.LoyaltyBenefit)
def loyalty_benefit_change(sender, instance, created, **kwargs):
    loyalty = instance.loyalty
    new_benefit = instance.benefit
    if not created and new_benefit:
        print('if not created and new_benefit:\n\n')
        number_of_bonuses = new_benefit.bonuses_to_add

        if number_of_bonuses:
            instance.loyalty.increase_balance(number_of_bonuses)
            to_balance_history = '\n'
            loyalty.balance_history = to_balance_history + loyalty.balance_history
            loyalty.save()
        if new_benefit.send_email_to_staff:
            text = 'todo send_email_staff Пользователем выбран, который должен выдать сотрудник '
            print(text)
            # todo send_email_staff

        loyalty.new_befits = len(list(user_models.LoyaltyBenefit.objects.filter(loyalty=loyalty,
            benefit=None)))
        loyalty.save()


@receiver(post_save, sender=models.Survey)
def auto_create_loyalty(sender, instance, created, **kwargs):
    if created:
        try:
            user_models.Loyalty.objects.create(user=instance.user)
            print('\nauto_create_loyalty\n')
        except Exception as e:
            # todo send_mail_admin
            print(e)




# # @receiver(m2m_changed, sender=models.Furniture)
@receiver(post_save, sender=models.Furniture)
def auto_recommendation(sender, instance, created, **kwargs):
    instance.check_recommendations()



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
