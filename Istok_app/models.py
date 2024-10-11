# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db import models
from django.core.validators import RegexValidator
from users import models as user_models
from django.utils import timezone
from PIL import Image
import os
from django.conf import settings
from . import validations as my_validations
from collections import Counter


#### Images and Files
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
#### Images and Files


#### Furniture +
class Furniture(models.Model):

    category = models.ForeignKey('FurnitureCategory', on_delete=models.CASCADE, verbose_name='Категория мебели')
    name = models.CharField(max_length=150, verbose_name='Название', unique=True)
    tags = models.ManyToManyField('Tags', through='FurnitureTags', related_name='tags',
        verbose_name='Теги')
    text = models.TextField(verbose_name='Описание мебели')
    price = models.PositiveIntegerField(verbose_name='Стоимость', default=1)
    images = models.ManyToManyField(ProjectImage, through='FurnitureImage', related_name='furniture_images',
        verbose_name='Изображения')
    #todo 3д доделать
    model_3d = models.CharField(null=True, blank=True, default='В РАЗРАБОТКЕ', max_length=20000,
        verbose_name='3D модель готовой мебели')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    recommendations = models.ManyToManyField('self', verbose_name='Список рекомендаций',
        through='SimilarFurniture', blank=True)


    def check_recommendations(self):
        if self.recommendations.all().count() < 3:
            recommendations = self.recommendations.all()
            default_rec_len = recommendations.count()
            lack_of_rec = 3 - default_rec_len
            print('default_rec_len == ', default_rec_len)
            print('lack_of_rec == ', lack_of_rec)
            ignore = list(recommendations.values_list('id', flat=True))
            similar = self.get_similar(num=lack_of_rec, ignore=ignore)
            print('recommendations== ', recommendations)
            print('similar == ', similar)
            new_set = recommendations.union(similar)
            print('new_set == ', new_set)
            for new in new_set:
                if SimilarFurniture.objects.filter(instance_furniture=self, similar_furniture=new).exists():
                    pass
                else:
                    SimilarFurniture.objects.create(instance_furniture=self, similar_furniture=new)





    def get_similar(self, num=3, ignore=None):
        """Получает список id мебели для игнорирования и необходимое количество похожей мебели для возврата.
        Возвращает кверисет из похожих объектов мебели (или случайных если нет достаточно объектов в той же категории).
        В лучшем случае только из своей категории с наибольшим совпадением тегов"""
        if ignore is None:
            ignore = []
        ignore.append(self.pk)
        similar_objs = Furniture.objects.filter(category=self.category, tags__in=self.tags.all()).exclude(pk__in=ignore)
        if similar_objs.count() < num:
            similar_objs = Furniture.objects.filter(category=self.category).exclude(pk__in=ignore)
        if similar_objs.count() < num:
            similar_objs = Furniture.objects.exclude(pk__in=ignore)
        similar_objs_dct = Counter(similar_objs.values_list('id', flat=True))
        sorted_similar = sorted(similar_objs_dct.items(), key=lambda item: item[1], reverse=True)[:num]
        pk_list = [_[0] for _ in sorted_similar]
        similar = Furniture.objects.filter(pk__in=pk_list)

        return similar


    class Meta:
        verbose_name = "Мебель"
        verbose_name_plural = "Готовая мебель для ознакомления"

    def get_tags(self):
        tags = self.tags.all()
        return ', '.join([tag.name for tag in tags])


    def __str__(self):
        return f'{self.name}(id={self.pk})'


class Tags(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    highlight = models.BooleanField(default=False, verbose_name='Визуальное выделение')

    def __str__(self):
        return f'{self.name}(id {self.pk})'

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


### m2m
class FurnitureTags(models.Model):
    furniture = models.ForeignKey('Furniture', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tags', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.furniture}: {self.tag}'

    class Meta:
        # Для уникальности м2м
        constraints = [
            models.UniqueConstraint(fields=['furniture', 'tag'], name='furniture_tag'),
        ]
        verbose_name = "Тег мебели"
        verbose_name_plural = "Теги для мебели"


class FurnitureCategory(models.Model):

    name = models.CharField(max_length=150, verbose_name='Название категории')


    def __str__(self):
        return f'Категория - {self.name}'


    class Meta:
        verbose_name = "Категория готовой мебели"
        verbose_name_plural = "Категории готовой мебели"


### m2m
class FurnitureImage(models.Model):
    furniture = models.ForeignKey('Furniture', on_delete=models.CASCADE)
    project_image = models.ForeignKey('ProjectImage', on_delete=models.CASCADE)

    def __str__(self):
        return f'Мебель({self.furniture.pk}) Изображение(id={self.project_image.pk})={self.project_image.image.path}'

    class Meta:
        # Для уникальности м2м
        constraints = [
            models.UniqueConstraint(fields=['furniture', 'project_image'], name='furniture_project_image'),
        ]
        verbose_name = "Изображение для мебели"
        verbose_name_plural = "Изображения для мебели"


### m2m
class SimilarFurniture(models.Model):
    instance_furniture = models.ForeignKey('Furniture', on_delete=models.CASCADE, related_name='instance_furniture')
    similar_furniture = models.ForeignKey('Furniture', on_delete=models.CASCADE, related_name='similar_furniture')

    def __str__(self):
        return f'К {self.instance_furniture.name} рекомендовать {self.similar_furniture.name}'

    class Meta:
        verbose_name = "Рекомендовать к этой мебели"
        verbose_name_plural = "Рекомендовать к этой мебели"
#### Furniture +


#### News
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
#### News


#### Order
def document_path(instance, filename):
    return f'documents/{instance.order.number}/{filename}'

class Order_Document(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='Заказ')
    file = models.FileField(upload_to=document_path, blank=True, verbose_name='Документ')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-time_created']
        verbose_name = "Документ"
        verbose_name_plural = "Документы заказа"

    def __str__(self):
        return f'{self.file.name}(id={self.pk})'


class Order_Image(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='Заказ')
    image = models.ImageField(verbose_name='Оригинальное изображение', upload_to=document_path)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-time_created']
        verbose_name = "(тех)Изображение"
        verbose_name_plural = "(тех)Изображения заказов"

    def __str__(self):
        return f'{self.image.name}(id={self.pk})'


class Order(models.Model):
    loyalty_code = models.CharField(max_length=5, blank=True, null=True, default=None,
        verbose_name='Чужой код лояльности',
        help_text='Если покупатель совершает заказ с использованием чужого кода лояльности, '
                  'владелец кода автоматически оповещается о возможности выбора выгоды')
    code_3d = '3d code'
    STATUSES = [
        ('Создан', 'Создан'),
        ('Выезд замерщика', 'Выезд замерщика'),
        ('Подготовка эскиза', 'Подготовка эскиза'),
        ('Монтаж', 'Монтаж'),
        ('Выполнен', 'Выполнен'),
        ('Отклонен', 'Отклонен'),
    ]
    #todo заменить на нового юзера потом
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')

    number = models.CharField(max_length=150, verbose_name='Номер заказа', unique=True)
    create_date = models.DateField(null=True, verbose_name='Дата заказа')
    shipment_date = models.DateField(null=True, blank=True, verbose_name='Дата доставки')
    status = models.CharField(max_length=100, choices=STATUSES, default='Создан', verbose_name='Статус заказа')
    address = models.CharField(max_length=150, verbose_name='Адрес доставки')

    # #todo сделать поле обязательным
    # documents = models.FileField(upload_to='contracts', blank=True, verbose_name='Договор')

    model_3d = models.CharField(null=True, blank=True, default=code_3d, max_length=20000,
        verbose_name='3D модель')
    # images = models.ManyToManyField(ProjectImage, through='OrderImage', related_name='order_images',
    #     verbose_name='Изображение заказа')

    #todo дополнительные документы и перечни.
    # additional_info =

    #todo настроить при наличии
    #

    def __str__(self):
        return f'{self.number}'


    class Meta:

        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


#### Application
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
#### Application


#todo !! перед завершением перенести эти модели в юзерс
#### Survey Опросник с готовыми ответами
class Answer(models.Model):
    text = models.TextField(verbose_name='Ответ', unique=True)
    user_answer = models.BooleanField(default=False, verbose_name='Ответ написан пользователем',
        help_text='Если True, то вариант был написан пользователем', blank=False)


    class Meta:
        verbose_name = "(Тех)Answer"
        verbose_name_plural = "(Тех)Answers"

    def __str__(self):
        return f'{self.text}'


class QuestionAndAnswer(models.Model):
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, verbose_name='Опросник', default=1)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='Вопрос')
    answers = models.ManyToManyField('Answer', through='AnswerQuestionAndAnswer',
        related_name='answers')


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['survey', 'question'], name='survey_question'),
        ]
        verbose_name = "(Тех)Вопрос с Ответом"
        verbose_name_plural = "(Тех)Вопросы с Ответами"

    def __str__(self):
        return f'{self.question.text}:\n' \
               f'{", ".join(list([_.text for _ in self.answers.all()]))}'


# m2m
class AnswerQuestionAndAnswer(models.Model):
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    question_and_answer = models.ForeignKey('QuestionAndAnswer', on_delete=models.CASCADE)


    def __str__(self):
        return f'({self.pk} Вопрос-{self.question_and_answer.question} Ответ-{self.answer.text}'

    class Meta:
        verbose_name = "(m2m)AnswerQuestionAndAnswer"
        verbose_name_plural = "(m2m)AnswerQuestionAndAnswers"


class Survey(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    # question_and_answers = models.ManyToManyField(QuestionAndAnswer, through='SurveyQuestionAndAnswer',
    #     related_name='question_and_answers', blank=False)
    dependable = models.BooleanField(default=True, verbose_name='Опросник надежен', blank=False,
        help_text='Статус становится положительным в случае если опросник заполняли '
                  'больше минимального времени заполнения. При аналитике ненадежные будут вычеркиваться из выборки')

    # questions_was_changed = models.BooleanField(default=False, verbose_name='(тех)Опросник был изменен', blank=True,
    #     help_text='Данный статус автоматически изменяется если были изменения в опроснике'
    #               '(как случай, добавление новых вопросов)\n'
    #               'Если есть новые вопросы пользователь должен будет вновь пройти опрос')
    new_questions = models.CharField(max_length=1000, verbose_name='(тех)Список id на неотвеченные вопросы',
        blank=True, default='')

    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата опроса')

    def __str__(self):
        return f'{self.user.full_name()} (id={self.user_id})'

    class Meta:
        verbose_name = "Опрос пользователя"
        verbose_name_plural = "Опросы пользователей"


    def check_questions(self):
        answered_questions = {_.question.pk for _ in self.questionandanswer_set.all()}
        all_questions = set(Question.objects.all().values_list('pk', flat=True))
        new_questions = ' '.join([str(_) for _ in all_questions.difference(answered_questions)])
        self.new_questions = new_questions
        self.save()
        return new_questions


    def show_info(self):
        num = len(self.questionandanswer_set.all())
        if self.dependable:
            text = f'Ответы на {num} вопросов.'
        else:
            text = f'НЕНАДЕЖЕН'
        return text

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
    multy_choice = models.BooleanField(default=False, verbose_name='Можно выбрать несколько',
        help_text='При включении этой опции позволяет опрашиваемому выбрать несколько вариантов')



    def __str__(self):
        return f'({self.pk}){self.text}'

    class Meta:
        verbose_name = "Вопрос для опросника"
        verbose_name_plural = "Вопросы для опросника"


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.pk} Вопрос({self.question.pk})/Ответ({self.option.pk}))'
#### Question Вопросы для опросника


#### Settings
class WebsiteSettings(models.Model):
    name = models.CharField(max_length=100, default='Все настройки', blank=True, verbose_name='')
    date_modified = models.DateTimeField(auto_now=True)
    min_write_time = models.PositiveIntegerField(default=30, verbose_name='Мин. время заполнения опросника(сек)',
    help_text='Минимальное количество времени, требуемое для заполнение опросника. Если опросник был заполнен быстрее, '
              'он будет помечен как неблагонадежный. Неблагонадежные опросники будут исключаться из аналитики.')

    def __str__(self):
        return f'Список настроек({self.pk}). Последнее изменение {self.date_modified}'

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"
#### Settings

