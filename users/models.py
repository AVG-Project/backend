from birthday import BirthdayField
from django.db import models
from django.contrib.auth.models import User
# from Istok_app.models import Orders


class Profile(models.Model):

    surname = models.CharField(max_length=30, unique=False, verbose_name='Отчество', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User джанго модели', primary_key=True)
    birth_date = BirthdayField(null=True, verbose_name='Дата рождения')
    mailing = models.BooleanField(default=False, verbose_name='Согласие на рассылку', blank=True)
    personal_data_processing = models.BooleanField(default=False, blank=True,
                                                   verbose_name='Согласие на обработку персональных данных')


    def __str__(self):
        return f'{self.user.username} Profile'


#todo вероятна уязвимость при редактировании полей опроса модели, путем изменения post ее могут привязать
# к другому пользователю, если редактирование модели будет происходит в одной въюшке.
# Возможно стоит выделить опросник в отдельную модель

PLANING_TIME = [
    ('0', 'Нет, не планирую'),
    ('1', 'Планирую, но не определился со временем'),
    ('2', 'Уже идет'),
    ('3', 'Скоро приступаем'),
    ('4', 'В течение полугода'),
    ('5', 'В течение года')
]

BONUS_CHOICE = [
    ('1', 'Скидка 10%\nДополнительная скидка при оплате техники или сантехники'),
    ('2', 'Скидка на столешницы SLOTEX\n'
          'Столешница Slotex - это влагостойкая ДСП, облицованная декоративным покрытием Slotex.'),
    ('3', 'Дополнительная скидка 5%\n'
          'Используйте дополнительную скидку для оплаты всего заказа.'
          '\nНе включает в себя стоимость доставки и сборки'),
    ('4', '10 000 рублей\nДенежными средствами (не на бонусный счёт)'),
    ('5', '15 000 рублей\nНа бонусный счёт (1 бонус = 1 рубль)'),
    ('6', '20 000 рублей\nМебель стоимость до 20 000 рублей в подарок')
]


class Loyalty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', primary_key=True)
    balance = models.IntegerField(default=0, verbose_name='Баланс')
    survey_repair = models.CharField(max_length=1, choices=PLANING_TIME, default='0',
        verbose_name='Планируете ли вы ремонт')
    survey_children = models.BooleanField(default=False, verbose_name='Есть ли у вас дети')
    bonus = models.CharField(max_length=1, choices=BONUS_CHOICE, default='1',
        verbose_name='Планируете ли вы ремонт', blank=True)
    card_number = models.CharField(max_length=19, verbose_name='Номер карты')
    loyalty_url = models.URLField(max_length=200, verbose_name='Ссылка для друга', blank=True)
    loyalty_code = models.CharField(max_length=20, verbose_name='Код программы лояльности')


    def __str__(self):
        return f'User.pk={self.user.pk} | Username={self.user.username} | Loyalty code={self.loyalty_code}'


    def increase_balance(self, order_cost: int) -> None:
        self.balance = self.balance + round(order_cost * 0.01)
        self.save()



# для быстрого подключения в консоли
# from django.contrib.auth.models import User
# from users.models import Loyalty, Profile
# from Istok_app.models import Orders
# u = User.objects.all().first()




#todo В дальнейшем реализую свою модель базового пользователя.
################
# from django.utils import timezone
# from django.forms import TextInput
# from django.contrib.auth.models import UserManager, PermissionsMixin
# from django.contrib.auth.base_user import AbstractBaseUser
# from django import forms
# from .validations import *
#
#
# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField("username",
#         max_length=12,
#         unique=True,
#         blank=False,
#         validators=[phone_regex],
#         error_messages={
#             "unique": "Пользователь с таким номером уже зарегистрирован.",
#         },
#     )
#
#     first_name = models.CharField("Имя", max_length=150, blank=False)
#     last_name = models.CharField("Фамилия", max_length=150, blank=False)
#     email = models.EmailField("Email", blank=False)
#     is_staff = models.BooleanField(
#         "staff status",
#         default=False,
#         help_text="Designates whether the user can log into this admin site.",
#     )
#     is_active = models.BooleanField(
#         "active",
#         default=True,
#         help_text="Designates whether this user should be treated as active. "
#                   "Unselect this instead of deleting accounts.",
#     )
#     date_joined = models.DateTimeField("date joined", default=timezone.now)
#
#     objects = UserManager()
#
#     EMAIL_FIELD = "email"
#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = ["email"]
#
#     class Meta:
#         verbose_name = "user"
#         verbose_name_plural = "users"
#         abstract = True
#
#     def clean(self):
#         super().clean()
#         self.email = self.__class__.objects.normalize_email(self.email)
#
#     def get_full_name(self):
#         """
#         Return the first_name plus the last_name, with a space in between.
#         """
#         full_name = "%s %s" % (self.first_name, self.last_name)
#         return full_name.strip()
#
#     def get_short_name(self):
#         """Return the short name for the user."""
#         return self.first_name
#
#     def email_user(self, subject, message, from_email=None, **kwargs):
#         """Send an email to this user."""
#         send_mail(subject, message, from_email, [self.email], **kwargs)
