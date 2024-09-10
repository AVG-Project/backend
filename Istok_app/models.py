from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from users.models import Loyalty
from django.utils import timezone
from PIL import Image
import os
from django.conf import settings


#todo Переделать. Не записывать урезанные картинки в бд, а резать и выдавать их при запросе в сериализаторе или вьюшке
class ProjectImage(models.Model):
    image = models.ImageField(verbose_name='Оригинальное изображение')
    image_medium = models.ImageField(verbose_name='Уменьшенное х2(Загрузка не требуется)', default=None, blank=True,
    help_text='Не загружать!')
    image_small = models.ImageField(verbose_name='Уменьшенное х5(Загрузка не требуется)', default=None, blank=True, help_text='Не загружать!')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    only_one_image = models.BooleanField(default=False, verbose_name='Создать только одно изображение', blank=True,
        help_text='Для готовой мебели опцию оставлять отключенной! '
                  'Для всего остального включать(это сократит занятое место на диске сервера)')


    def __str__(self):
        return f'id={self.pk} | name={self.image.name}'

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def save(self, *args, **kwargs):
        super(ProjectImage, self).save(*args, **kwargs)
        if not self.only_one_image:
            if self.image and not self.image_medium and not self.image_small:
                self.image_medium = self.reduce_image(2)
                self.image_small = self.reduce_image(5)
                self.save()
            elif self.image.name not in self.image_medium.name:
                self.image_medium = self.reduce_image(2)
                self.image_small = self.reduce_image(5)
                self.save()

    def reduce_image(self, rate: int) -> str:

        image = Image.open(self.image.path)
        name = self.image.name
        file_name = os.path.splitext(name)[0]
        file_format = os.path.splitext(name)[1]
        if rate > 2:
            size_name = 'small_'
        else:
            size_name = 'medium_'
        new_name = size_name + file_name + file_format
        path = self.image.path[:(len(name)*-1)] + new_name
        size = (image.size[0] // rate, image.size[1] // rate)
        image = image.resize(size)
        image.save(path)
        return new_name


class Tags(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    highlight = models.BooleanField(default=False, verbose_name='Визуальное выделение')

    def __str__(self):
        return f'{self.name}(id {self.pk}) Подсветка: {self.highlight}'

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class FurnitureCategory(models.Model):

    name = models.CharField(max_length=150, verbose_name='Название категории')


    def __str__(self):
        return f'Категория - {self.name}'


    class Meta:
        verbose_name = "Категория готовой мебели"
        verbose_name_plural = "Категории готовой мебели"



class Furniture(models.Model):

    category = models.ForeignKey(FurnitureCategory, on_delete=models.CASCADE, verbose_name='Категория мебели')
    name = models.CharField(max_length=150, verbose_name='Название')
    tags = models.ManyToManyField(Tags, through='FurnitureTags', related_name='tags',
        verbose_name='Теги')
    text = models.TextField(verbose_name='Описание мебели')
    price = models.PositiveIntegerField(verbose_name='Стоимость', default=1)
    images = models.ManyToManyField(ProjectImage, through='FurnitureImage', related_name='furniture_images',
        verbose_name='Изображения')
    #todo 3д доделать
    model_3d = models.CharField(null=True, blank=True, default='В РАЗРАБОТКЕ', max_length=20000,
        verbose_name='3D модель готовой мебели')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


    class Meta:
        verbose_name = "Мебель"
        verbose_name_plural = "Готовая мебель для ознакомления"


    def get_tags(self):
        tags = self.tags.all()

        return ', '.join([tag.name for tag in tags])


    def __str__(self):
        return f'{self.name}(id={self.pk})'


class News(models.Model):
    title = models.TextField(verbose_name='Титульная часть новости')
    text = models.TextField(verbose_name='Текст новости')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    image = models.ImageField(verbose_name='Изображение', blank=True)
    extra_url = models.URLField(verbose_name='Ссылка на внешний источник', default='', blank=True)


    def __str__(self):
        return f'{self.title[:15]}|Дата: {self.time_created.date()}'


    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"



class Order(models.Model):
    code_3d = '<div class="sketchfab-embed-wrapper"> ' \
              '<iframe title="3D" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" ' \
              'allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking ' \
              'execution-while-out-of-viewport execution-while-not-rendered web-share ' \
              'src="https://sketchfab.com/models/b4ec7831bb3e416c841c50b88c1bea16/embed"> ' \
              '</iframe> <p style="font-size: 13px; font-weight: normal; margin: 5px; ' \
              'color: #4A4A4A;"> <a href="https://sketchfab.com/3d-models/3d-b4ec7831bb3e416c841c50b88c1bea16?utm_' \
              'medium=embed&utm_campaign=share-popup&utm_content=b4ec7831bb3e416c841c50b88c1bea16" target="_blank" ' \
              'rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> 3D </a> by ' \
              '<a href="https://sketchfab.com/ki1004ka?utm_medium=embed&utm_campaign=share-popup&utm_content=' \
              'b4ec7831bb3e416c841c50b88c1bea16" target="_blank" rel="nofollow" style="font-weight: bold; ' \
              'color: #1CAAD9;"> Alexander Vasiliev </a> on ' \
              '<a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=' \
              'b4ec7831bb3e416c841c50b88c1bea16" target="_blank" rel="nofollow" style="font-weight: ' \
              'bold; color: #1CAAD9;">Sketchfab</a></p></div>'
    STATUSES = [
        ('1', 'Создан'),
        ('2', 'Выезд замерщика'),
        ('3', 'Подготовка эскиза'),
        ('4', 'Монтаж'),
        ('5', 'Выполнен'),
        ('6', 'Отклонен'),
    ]
    #todo заменить на нового юзера потом
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')

    number = models.CharField(max_length=150, verbose_name='Номер заказа')
    create_date = models.DateField(null=True, verbose_name='Дата заказа')
    shipment_date = models.DateField(null=True, blank=True, verbose_name='Дата доставки')
    status = models.CharField(max_length=1, choices=STATUSES, default='1', verbose_name='Статус заказа')
    address = models.CharField(max_length=150, verbose_name='Адрес доставки')
    contract = models.FileField(upload_to='contracts', blank=True, verbose_name='Договор')
    model_3d = models.CharField(null=True, blank=True, default=code_3d, max_length=20000,
        verbose_name='3D модель')
    images = models.ManyToManyField(ProjectImage, through='OrderImage', related_name='order_images',
        verbose_name='Изображение заказа')

    #todo дополнительные документы и перечни.
    # additional_info =

    #todo настроить при наличии
    # loyalty_code = models.ForeignKey(Loyalty, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'ID={self.pk} | user={self.user.pk} | number={self.number}'


    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"



class Application(models.Model):

    PHONE_REGEX = RegexValidator(
        regex=r'^\+?1?\d{9,13}$',
        message="Телефон должен быть указан в формате: "
                "'+7ХХХХХХХХХХ'. Максимум 13 символов.")

    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Пользователь', null=True, blank=True)

    text = models.TextField(blank=False, verbose_name='Дополнительная информация')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    patronymic = models.CharField(null=True, blank=True, max_length=150, verbose_name='Отчество')
    phone = models.CharField(validators=[PHONE_REGEX], max_length=13,
                             blank=False, verbose_name='Ваш номер телефона')
    contact_type = models.CharField(null=True, blank=True, max_length=150, verbose_name='Как с Вами связаться?')
    link = models.CharField(null=True, blank=True, max_length=150, verbose_name='Ваша ссылка на Telegram/ВКонтакте')
    date_time = models.CharField(null=True, blank=True, max_length=30, verbose_name='Дата и время встречи')

    python_date_time = models.DateTimeField(null=True, blank=True,
        verbose_name='Для теста перевода формата времени из js в python')


    def __str__(self):
        return f'ID={self.pk} | phone={self.phone}'

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки пользователей"






#### Survey Опросник с готовыми ответами
class Answer(models.Model):
    text = models.TextField(verbose_name='Ответ')
    user_answer = models.BooleanField(default=False, verbose_name='Ответ написан пользователем',
        help_text='Если True, то вариант был написан пользователем', blank=False)


    class Meta:
        verbose_name = "(Тех)Answer"
        verbose_name_plural = "(Тех)Answers"

    def __str__(self):
        return f'Ответ({self.pk}) - {self.text}'


class QuestionAndAnswer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='Вопрос')
    answers = models.ManyToManyField('Answer', through='AnswerQuestionAndAnswer',
        related_name='answers')
    # user_answer = models.BooleanField(default=False, verbose_name='Ответ написан пользователем',
    #     help_text='Если True, то вариант не был написан пользователем')


    class Meta:
        verbose_name = "(Тех)QuestionAndAnswer"
        verbose_name_plural = "(Тех)QuestionAndAnswers"

    def __str__(self):
        return f'Вопрос-ответ({self.pk}) {self.question}'


# Many_to_many
class AnswerQuestionAndAnswer(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question_and_answer = models.ForeignKey('QuestionAndAnswer', on_delete=models.CASCADE)


    def __str__(self):
        return f'({self.pk} Вопрос-{self.question_and_answer.question} Ответ-{self.answer.text}'

    class Meta:
        verbose_name = "(m2m)AnswerQuestionAndAnswer"
        verbose_name_plural = "(m2m)AnswerQuestionAndAnswers"


class Survey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Пользователь', null=True, blank=True)
    question_and_answers = models.ManyToManyField(QuestionAndAnswer, through='SurveyQuestionAndAnswer',
        related_name='question_and_answers', blank=False)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата опроса')

    def __str__(self):
        return f'({self.pk})|User={self.user.pk}'

    class Meta:
        verbose_name = "Опрос пользователя"
        verbose_name_plural = "Опросы пользователей"


# Many_to_many
class SurveyQuestionAndAnswer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_and_answer = models.ForeignKey(QuestionAndAnswer, on_delete=models.CASCADE)


    def __str__(self):
        return f'({self.pk} Опрос({self.survey.pk})'

    class Meta:
        verbose_name = "(m2m)Ответ на вопрос"
        verbose_name_plural = "(m2m)Ответы на вопросы"
#### Survey Опросник с готовыми ответами



#### Question Вопросы для опросника

class Option(models.Model):
    text = models.CharField(max_length=200, verbose_name='Текст варианта ответа')
    user_input = models.BooleanField(default=False, verbose_name='Вариант пользователя',
        help_text='Если True, пользователь сможет ввести свой вариант ответа')

    def __str__(self):
        return f'({self.pk}) {self.text})'

    class Meta:
        verbose_name = "(Тех)Option"
        verbose_name_plural = "(Тех)Options"


class Question(models.Model):
    text = models.TextField(verbose_name='Вопрос')
    options = models.ManyToManyField(Option, through='QuestionOption', related_name='options')
    multy_choice = models.BooleanField(default=False, verbose_name='Выбрать несколько ответов',
        help_text='При включении этой опции позволяет опрашиваемому выбрать несколько вариантов')

    def __str__(self):
        return f'({self.pk}){self.text}'

    class Meta:
        verbose_name = "Вопрос с вариантами ответа"
        verbose_name_plural = "Вопросы с вариантами ответа"


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.pk} Вопрос({self.question.pk})/Ответ({self.option.pk}))'


#### Question Вопросы для опросника



####### Промежуточные таблицы для ManyToMany
class FurnitureTags(models.Model):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.furniture}: {self.tag}'

    class Meta:
        # Для уникальности м2м
        constraints = [
            models.UniqueConstraint(fields=['furniture', 'tag'], name='furniture_tag'),
        ]
        verbose_name = "Тег мебели"
        verbose_name_plural = "Теги для мебели"


class FurnitureImage(models.Model):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    project_image = models.ForeignKey(ProjectImage, on_delete=models.CASCADE)

    def __str__(self):
        return f'Мебель({self.furniture.pk}) Изображение(id={self.project_image.pk})={self.project_image.image.path}'

    class Meta:
        # Для уникальности м2м
        constraints = [
            models.UniqueConstraint(fields=['furniture', 'project_image'], name='furniture_project_image'),
        ]
        verbose_name = "Изображение для мебели"
        verbose_name_plural = "Изображения для мебели"

class OrderImage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_image = models.ForeignKey(ProjectImage, on_delete=models.CASCADE)

    def __str__(self):
        return f'Номер заказа - {self.order.pk} | Название изображения - {self.order_image.image.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'order_image'], name='order_order_image'),
        ]
        verbose_name = "Изображение для заказа"
        verbose_name_plural = "Изображения для заказа"


####### Старое

# class Description(models.Model):
#
#     part_number = models.PositiveIntegerField(verbose_name='Порядковый номер части текста')
#     text = models.TextField(default='Нет описание мебели', verbose_name='Описание мебели')
#
#
#     def __str__(self):
#         return f"(id={self.pk}){self.text[0:20]}..."
#
#     class Meta:
#         verbose_name = "Текст"
#         verbose_name_plural = "Тексты"


# class Parts(models.Model):
#
#     PARTS_TYPE = [
#         ('1', 'Корпус'),
#         ('2', 'Фасад'),
#         ('3', 'Петли'),
#         ('4', 'Ручки'),
#         ('5', 'Направляющие'),
#         ('6', 'Столешница'),
#         ('7', 'Цоколь'),
#         ('8', 'Опоры'),
#         ('9', 'Стеновая панель'),
#         ('10', 'Аксесуары'),
#         ('11', 'Сантехника'),
#         ('12', 'Бытовая техника'),
#     ]
#
#     UNIT = [
#         ('1', 'шт.'),
#         ('2', 'м'),
#         ('3', 'кв.м'),
#         ('4', 'пог.м'),
#     ]
#
#     order_number = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Номер заказа')
#     parts_type = models.CharField(max_length=5, choices=PARTS_TYPE, default=None, verbose_name='Тип комплектующих')
#     parts_name = models.CharField(max_length=200, verbose_name='Наименование')
#     parts_unit = models.CharField(max_length=1, choices=UNIT, default=None, verbose_name='Единица измерения')
#     parts_quantity = models.FloatField(verbose_name='Количество')
#     parts_price = models.FloatField(verbose_name='Цена')
#     parts_image = models.ImageField(default='default_mebel.jpg', verbose_name='Изображение')


# from Istok_app.models import *



# class Furniture(models.Model):
#
#     TYPES = [
#         ('1', 'Кухня'),
#         ('2', 'Гардероб'),
#         ('3', 'Комоды'),
#         ('4', 'Комод'),
#         ('5', 'Тумбочка'),
#         ('6', 'Шкаф'),
#         ('7', 'Прихожая'),
#         ('8', 'Системы хранения'),
#         ('9', 'Стеллаж'),
#     ]
#
#     FORMS = [
#         ('0', 'Нет данных'),
#         ('1', 'Прямая'),
#         ('2', 'Г-образная'),
#         ('3', 'П-образная'),
#         ('4', 'С барной стойкой'),
#         ('5', 'С островом'),
#     ]
#
#     MATERIAL = [
#         ('1', 'ЛДСП'),
#         ('2', 'МДФ'),
#         ('3', 'Пленка ПВХ'),
#         ('4', 'Пластик AGT'),
#         ('5', 'Пластик Fenix'),
#         ('6', 'Эмаль'),
#     ]
#
#     STYLES = [
#         ('1', 'Классика'),
#         ('2', 'Современный'),
#         ('3', 'Лофт'),
#         ('4', 'Скандинавский'),
#         ('5', 'Минимализм'),
#         ('6', 'Хай-тек'),
#         ('7', 'Прованс'),
#         ('8', 'Кантри'),
#     ]
#
#     TABLETOP_MATERIAL = [
#         ('1', 'Столешница ДСП с покрытием HPL'),
#         ('2', 'Столешница компакт-ламинат'),
#         ('3', 'Кварцевая столешница'),
#         ('4', 'Акриловая столешница'),
#         ('5', 'Пластик Fenix')
#     ]
#
#     name = models.CharField(max_length=150, verbose_name='Название')
#     type = models.CharField(max_length=2, choices=TYPES, default='1', verbose_name='Тип мебели')
#     form = models.CharField(max_length=2, choices=FORMS, default='1', verbose_name='Форма мебели')
#     style = models.CharField(max_length=2, choices=STYLES, default='1', verbose_name='Стиль мебели')
#     body_material = models.CharField(max_length=2, choices=MATERIAL, default='1', verbose_name='Материал корпуса')
#     facades_material = models.CharField(max_length=2, choices=MATERIAL, default='1', verbose_name='Материал фасадов')
#     tabletop_material = models.CharField(max_length=2, choices=TABLETOP_MATERIAL, default='1',
#         verbose_name='Материал столешницы')
#     price = models.PositiveIntegerField(verbose_name='Стоимость', default=1)
#     time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
#     text = models.TextField(verbose_name='Описание мебели')
#
#     tags = models.ManyToManyField(Tags, through='FurnitureTags', related_name='tags',
#         verbose_name='Теги')
#     purposes = models.ManyToManyField(Purpose, through='FurniturePurpose', related_name='purposes',
#         verbose_name='Назначения')
#     images = models.ManyToManyField(ProjectImage, through='FurnitureImage', related_name='furniture_images',
#         verbose_name='Изображения')
#
#     class Meta:
#         verbose_name = "Мебель"
#         verbose_name_plural = "Вся мебель"
#
#     def get_tags(self):
#         tags = self.tags.all()
#
#         return ', '.join([tag.name for tag in tags])
#
#     def __str__(self):
#         return f'{self.name}(id={self.pk})'
