from django.core.mail import send_mail
from django.db.models.signals import post_save, m2m_changed, post_delete, pre_delete
from django.dispatch import receiver

from Istok.settings import SERVER_EMAIL
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
                subject = 'Компания ИСТОК'
                message = f'Вашим кодом лояльности воспользовались при оформлении заказа!\n' \
                          f'Вам доступен выбор "Выгоды" на странице лояльности в личном кабинете.'

                print(subject, message, [friends_loyalty.user.email], sep='\n')
                # todo Включить
                # send_mail(subject, message, SERVER_EMAIL, [friends_loyalty.user.email])

            except Exception as e:
                send_email('Istok_app.signals.create_order()', e, SERVER_EMAIL, SERVER_EMAIL)
        elif not friends_loyalty:
            subject = f'Указанный код лояльности в заказе отсутствует.'
            message = f'В заказе {instance.number}, был указан код лояльности: {friends_code}.' \
                      f'Данный код отсутствует в базе данных. Вероятно заказчик неправильно указал его.'

            print(subject, message, user_models.staff_email_list(), sep='\n')
            # todo Включить
            # send_mail(subject, message, SERVER_EMAIL, user_models.staff_email_list())
        else:
            subject = f'Указанный код уже был использован.'
            message = f'В заказе {instance.number}, был указан код лояльности: {friends_code}.' \
                      f'Так как данным кодом уже воспользовались награда не будет выдана.'

            print(subject, message, user_models.staff_email_list(), sep='\n')
            # todo Включить
            # send_mail(subject, message, SERVER_EMAIL, user_models.staff_email_list())


@receiver(post_save, sender=user_models.LoyaltyBenefit)
def loyalty_benefit_change(sender, instance, created, **kwargs):
    loyalty = instance.loyalty
    new_benefit = instance.benefit
    if not created and new_benefit:
        number_of_bonuses = new_benefit.bonuses_to_add

        if number_of_bonuses:
            instance.loyalty.increase_balance(number_of_bonuses)
            to_balance_history = '\n'
            loyalty.balance_history = to_balance_history + loyalty.balance_history
            loyalty.save()
        if new_benefit.send_email_to_staff:
            subject = f'Пользователь сайта выбрал бонус.'
            message = f'Пользователь сайта {loyalty.user.email}, выбрал бонус: {new_benefit}.' \
                      f'Данный бонус может быть выбран только сотрудником.' \
                      f'После выдачи или отклонения выдачи бонуса не забудьте сменить статус в поле ' \
                      f'(m2m) Выбранная выгода с (id{instance.pk})'
            print(subject, message, user_models.staff_email_list(), sep='\n')
            # todo Включить
            # send_mail(subject, message, SERVER_EMAIL, user_models.staff_email_list())

        loyalty.new_befits = len(list(user_models.LoyaltyBenefit.objects.filter(loyalty=loyalty,
            benefit=None)))
        loyalty.save()


@receiver(post_save, sender=models.Survey)
def auto_create_loyalty(sender, instance, created, **kwargs):
    if created:
<<<<<<< Updated upstream
        try:
            user_models.Loyalty.objects.create(user=instance.user)
            print('\nauto_create_loyalty\n')
        except Exception as e:
            # todo send_mail_admin
            print(e)
=======
        if not user_models.Loyalty.objects.filter(user=instance.user).exists():
            try:
                user_models.Loyalty.objects.create(user=instance.user)
                print('\nauto_create_loyalty\n')
            except Exception as e:
                subject = f'auto_create_loyalty'
                print(subject, e, sep='\n')
                # todo Включить
                # send_mail(subject, e, SERVER_EMAIL, SERVER_EMAIL)
>>>>>>> Stashed changes




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

#todo доделать оправку заказа на связь

@receiver(post_save, sender=models.Application)
def send_application_email(sender, instance, created, **kwargs):

    # instance = models.Application.objects.first()
    if created:
        subject = 'Новая заявка.'
        message = f'''
            Пользователь формил заявку. 
            (Пользователь {'Не зарегистрирован' if not instance.user else f'Зарегистрирован - {instance.user.email}'})
            ФИО - {instance.last_name.capitalize()} {instance.first_name.capitalize()}
            Номер телефона: {instance.phone}
            Тип связи: {instance.contact_type}
            Ссылка: {instance.link}
            Дата и время: {instance.date_time.strftime("%d.%m.%Y в %H:%M")}
            Дополнительная информация:
            {instance.text}
        '''
        print(f'send_mail {user_models.staff_email_list()}')
        print(message)
        # todo Включить
        # todo сделать проверку на наличие сотрудников
        # send_mail(subject, message, SERVER_EMAIL, user_models.staff_email_list())
