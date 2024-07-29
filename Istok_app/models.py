from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from users.models import Loyalty
from django.utils import timezone
from PIL import Image
import os
from django.conf import settings


class ProjectImage(models.Model):
    image = models.ImageField(verbose_name='Оригинальное изображение')
    image_medium = models.ImageField(verbose_name='Оригинальное изображение', default=None, blank=True)
    image_small = models.ImageField(verbose_name='Оригинальное изображение', default=None, blank=True)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    only_one_image = models.BooleanField(default=False, verbose_name='Создать только одно изображение', blank=True)


    def save(self, *args, **kwargs):
        super(ProjectImage, self).save(*args, **kwargs)
        if self.image and not self.image_medium and not self.image_small and not self.only_one_image:
            self.image_medium = self.reduce_image(2)
            self.image_small = self.reduce_image(5)
            self.save()
        elif self.image.name not in self.image_medium.name and not self.only_one_image:
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



class Purpose(models.Model):
    name = models.CharField(max_length=60, unique=True)


    def __str__(self):
        return f"id={self.pk}, Назначение={self.name}"

    class Meta:
        verbose_name = "Назначение мебели"
        verbose_name_plural = "Назначения мебели"


class Tags(models.Model):
    name = models.CharField(max_length=40, unique=True)
    highlight = models.BooleanField(default=False, verbose_name='Визуальное выделение')

    def __str__(self):
        return f'{self.name} Подсветка: {self.highlight}'

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Description(models.Model):
    part_number = models.PositiveIntegerField(verbose_name='Порядковый номер части текста')
    text = models.TextField(default='Нет описание мебели', verbose_name='Описание мебели')


    def __str__(self):
        return f"(id={self.pk}){self.text[0:20]}..."

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"


class Furniture(models.Model):
    #todo создать для каждого выбора внешний ключ на таблицу
    TYPES = [
        ('1', 'Кухня'),
        ('2', 'Гардероб'),
        ('3', 'Стол'),
        ('4', 'Комод'),
        ('5', 'Тумбочка'),
        ('6', 'Шкаф'),
        ('7', 'Прихожая'),
        ('8', 'Системы хранения'),
        ('9', 'Стеллаж'),
    ]

    FORMS = [
        ('0', 'Нет данных'),
        ('1', 'Прямая'),
        ('2', 'Г-образная'),
        ('3', 'П-образная'),
        ('4', 'С барной стойкой'),
        ('5', 'С островом'),
    ]

    MATERIAL = [
        ('1', 'ЛДСП'),
        ('2', 'МДФ'),
        ('3', 'Пленка ПВХ'),
        ('4', 'Пластик AGT'),
        ('5', 'Пластик Fenix'),
        ('6', 'Эмаль'),
    ]

    STYLES = [
        ('1', 'Классика'),
        ('2', 'Современный'),
        ('3', 'Лофт'),
        ('4', 'Скандинавский'),
        ('5', 'Минимализм'),
        ('6', 'Хай-тек'),
        ('7', 'Прованс'),
        ('8', 'Кантри'),
    ]

    TABLETOP_MATERIAL = [
        ('1', 'Столешница ДСП с покрытием HPL'),
        ('2', 'Столешница компакт-ламинат'),
        ('3', 'Кварцевая столешница'),
        ('4', 'Акриловая столешница'),
        ('5', 'Пластик Fenix')
    ]

    name = models.CharField(max_length=150, verbose_name='Название')
    type = models.CharField(max_length=2, choices=TYPES, default='1', verbose_name='Тип мебели')
    form = models.CharField(max_length=2, choices=FORMS, default='1', verbose_name='Форма мебели')
    style = models.CharField(max_length=2, choices=STYLES, default='1', verbose_name='Стиль мебели')
    body_material = models.CharField(max_length=2, choices=MATERIAL, default='1', verbose_name='Материал корпуса')
    facades_material = models.CharField(max_length=2, choices=MATERIAL, default='1', verbose_name='Материал фасадов')
    tabletop_material = models.CharField(max_length=2, choices=TABLETOP_MATERIAL, default='1', verbose_name='Материал столешницы')
    price = models.PositiveIntegerField(verbose_name='Стоимость', default=1)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    text = models.TextField(verbose_name='Описание мебели')
    
    tags = models.ManyToManyField(Tags, through='FurnitureTags', related_name='tags',
        verbose_name='Теги')
    purposes = models.ManyToManyField(Purpose, through='FurniturePurpose', related_name='purposes',
        verbose_name='Назначения')
    images = models.ManyToManyField(ProjectImage, through='FurnitureImage', related_name='images',
        verbose_name='Теги')





    class Meta:
        verbose_name = "Мебель"
        verbose_name_plural = "Вся мебель"


    def get_tags(self):
        tags = self.tags.all()

        return ', '.join([tag.name for tag in tags])


    def __str__(self):
        return f'{self.name}(id={self.pk})'

####### Промежуточные таблицы для ManyToMany
class FurnitureTags(models.Model):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.furniture}: {self.tag}'


class FurniturePurpose(models.Model):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.furniture}| Назначение: {self.purpose}'


class FurnitureImage(models.Model):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    project_image = models.ForeignKey(ProjectImage, on_delete=models.CASCADE)

    def __str__(self):
        return f'Мебель({self.furniture.pk}) Изображение(id={self.project_image.pk})={self.project_image.image.path}'
#######


class Application(models.Model):

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,12}$',
        message="Телефон должен быть указан в формате: "
                "'+7ХХХХХХХХХХ'. Максимум 12 символов.")

    type = models.CharField(null=True, blank=True, max_length=150, verbose_name='Тип мебели')
    form = models.CharField(null=True, blank=True, max_length=150, verbose_name='Форма мебели')
    addition = models.CharField(null=True, blank=True, max_length=150, verbose_name='Дополнения')
    facades_material = models.CharField(null=True, blank=True, max_length=150, verbose_name='Материал фасада')
    table_material = models.CharField(null=True, blank=True, max_length=150, verbose_name='Материал столешницы')
    plumb = models.CharField(null=True, blank=True, max_length=150, verbose_name='Кухонная сантехника')
    appliances = models.CharField(null=True, blank=True, max_length=150, default=None, verbose_name='Бытовая техника')
    budget = models.CharField(null=True, blank=True, max_length=150, verbose_name='Бюджет проекта')
    consultation = models.CharField(null=True, blank=True, max_length=150,
                                    verbose_name='Консультация с экспертом по обустройству дома')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    patronymic = models.CharField(null=True, blank=True, max_length=150, verbose_name='Отчество')
    phone = models.CharField(validators=[phone_regex], max_length=12,
                             blank=False, verbose_name='Ваш номер телефона')
    connection = models.CharField(null=True, blank=True, max_length=150, verbose_name='Как с Вами связаться?')
    link = models.CharField(null=True, blank=True, max_length=150, verbose_name='Ваша ссылка на Telegram/ВКонтакте')
    data = models.CharField(null=True, blank=True, max_length=30, verbose_name='Дата')
    time = models.CharField(null=True, blank=True, max_length=30, verbose_name='Время')


class Orders(models.Model):
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
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Номер телефона')
    order_number = models.CharField(null=True, blank=True, max_length=150, verbose_name='Номер заказа')
    order_date = models.DateField(null=True, blank=True, verbose_name='Дата заказа')
    order_shipment_date = models.DateField(null=True, blank=True, verbose_name='Дата доставки')
    order_status = models.CharField(max_length=1, choices=STATUSES, default='1', verbose_name='Статус заказа')
    order_delivery_address = models.CharField(null=True, blank=True, max_length=150, verbose_name='Адрес доставки')
    order_contract = models.FileField(upload_to='Contrac', blank=True, verbose_name='Договор')
    order_price = models.FloatField(null=True, blank=True, verbose_name='Стоимость заказа')
    order_sketch1 = models.ImageField(null=True, blank=True, default=None, verbose_name='Эскиз1')
    order_sketch2 = models.ImageField(null=True, blank=True, default=None, verbose_name='Эскиз2')
    order_sketch3 = models.ImageField(null=True, blank=True, default=None, verbose_name='Эскиз3')
    order_sketch4 = models.ImageField(null=True, blank=True, default=None, verbose_name='Эскиз4')
    order_3D_model = models.CharField(null=True, blank=True, default=code_3d, max_length=20000, verbose_name='3D модель')
    order_by_loyalty_code = models.ForeignKey(Loyalty, models.SET_NULL, blank=True, null=True)


class Parts(models.Model):

    PARTS_TYPE = [
        ('1', 'Корпус'),
        ('2', 'Фасад'),
        ('3', 'Петли'),
        ('4', 'Ручки'),
        ('5', 'Направляющие'),
        ('6', 'Столешница'),
        ('7', 'Цоколь'),
        ('8', 'Опоры'),
        ('9', 'Стеновая панель'),
        ('10', 'Аксесуары'),
        ('11', 'Сантехника'),
        ('12', 'Бытовая техника'),
    ]

    UNIT = [
        ('1', 'шт.'),
        ('2', 'м'),
        ('3', 'кв.м'),
        ('4', 'пог.м'),
    ]

    order_number = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Номер заказа')
    parts_type = models.CharField(max_length=5, choices=PARTS_TYPE, default=None, verbose_name='Тип комплектующих')
    parts_name = models.CharField(max_length=200, verbose_name='Наименование')
    parts_unit = models.CharField(max_length=1, choices=UNIT, default=None, verbose_name='Единица измерения')
    parts_quantity = models.FloatField(verbose_name='Количество')
    parts_price = models.FloatField(verbose_name='Цена')
    parts_image = models.ImageField(default='default_mebel.jpg', verbose_name='Изображение')


# from Istok_app.models import *

