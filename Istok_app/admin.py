from django.contrib import admin
from Istok_app import models



istok_app_models = [models.Tags, models.News, models.ProjectImage, models.Application, models.FurnitureCategory,
                    models.Option, models.Answer, models.Order_Document]

admin.site.register(istok_app_models)


#### Settings
@admin.register(models.WebsiteSettings)
class WebsiteSettingsAdmin(admin.ModelAdmin):
    model = models.WebsiteSettings
    list_display = ['name']


    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
#### Settings


#### Furniture
class TagsInstanceInline(admin.TabularInline):
    model = models.FurnitureTags

class ImageInstanceInline(admin.TabularInline):
    model = models.FurnitureImage

class SimilarFurnitureInline(admin.TabularInline):
    model = models.SimilarFurniture
    fk_name = 'instance_furniture'


@admin.register(models.Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    model = models.Furniture
    list_display = ['category', 'name', 'id', "get_tags"]
    inlines = [TagsInstanceInline, ImageInstanceInline, SimilarFurnitureInline]
#### Furniture


#### Order
class OrderImagesInline(admin.TabularInline):
    model = models.Order_Image

class OrderDocsInline(admin.TabularInline):
    model = models.Order_Document

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    list_display = ['number', 'user', 'id', 'create_date', 'shipment_date', 'status', 'address']
    inlines = [OrderImagesInline, OrderDocsInline]
#### Order


#### Question
class QuestionOptionInline(admin.TabularInline):
    model = models.QuestionOption

@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    model = models.Question
    list_display = ['text', 'id']
    inlines = [QuestionOptionInline]
#### Question


#### QuestionAndAnswer
# class AnswerQuestionAndAnswerInline(admin.TabularInline):
#     model = models.AnswerQuestionAndAnswer
#
# @admin.register(models.QuestionAndAnswer)
# class QuestionAndAnswerAdmin(admin.ModelAdmin):
#     model = models.QuestionAndAnswer
#     list_display = ['survey', 'question', 'id']
#     inlines = [AnswerQuestionAndAnswerInline]
#
#     def has_change_permission(self, request, obj=None):
#         return False
#### QuestionAndAnswer


#### Survey
class QuestionAndAnswerInline(admin.TabularInline):
    model = models.QuestionAndAnswer
    can_delete = False
    fields = ['__str__']
    readonly_fields = ['__str__']

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(models.Survey)
class SurveyAdmin(admin.ModelAdmin):
    model = models.Survey
    list_display = ['user', 'time_created', 'show_info']
    inlines = [QuestionAndAnswerInline]

    # def has_change_permission(self, request, obj=None):
    #     return False
#### Survey




