from django.contrib import admin

from Istok_app import models



istok_app_models = [models.Tags, models.News, models.ProjectImage, models.Application, models.FurnitureCategory,
                    models.Option, models.Answer]

admin.site.register(istok_app_models)




# class FurnitureInline(admin.TabularInline):
#     model = Furniture.tags.through
#
#
# @admin.register(Tags)
# class TagsAdmin(admin.ModelAdmin):
#     model = Tags
#     inlines = [
#         FurnitureInline,
#     ]

#### Furniture
class TagsInstanceInline(admin.TabularInline):
    model = models.FurnitureTags

class ImageInstanceInline(admin.TabularInline):
    model = models.FurnitureImage

@admin.register(models.Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    model = models.Furniture
    list_display = ['category', 'name', 'id', "get_tags"]
    inlines = [TagsInstanceInline, ImageInstanceInline]
#### Furniture


#### Order
class OrderImagesInline(admin.TabularInline):
    model = models.OrderImage

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    list_display = ['number', 'user', 'id', 'create_date', 'shipment_date', 'status', 'address']
    inlines = [OrderImagesInline]
#### Order


#### Order
class QuestionOptionInline(admin.TabularInline):
    model = models.QuestionOption

@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    model = models.Question
    list_display = ['text', 'id']
    inlines = [QuestionOptionInline]
#### Order


#### QuestionAndAnswer
class AnswerQuestionAndAnswerInline(admin.TabularInline):
    model = models.AnswerQuestionAndAnswer

@admin.register(models.QuestionAndAnswer)
class QuestionAndAnswerAdmin(admin.ModelAdmin):
    model = models.QuestionAndAnswer
    list_display = ['question', 'id']
    inlines = [AnswerQuestionAndAnswerInline]
#### QuestionAndAnswer


#### Survey
class SurveyQuestionAndAnswerInline(admin.TabularInline):
    model = models.SurveyQuestionAndAnswer

@admin.register(models.Survey)
class SurveyAdmin(admin.ModelAdmin):
    model = models.Survey
    list_display = ['user', 'id', 'time_created']
    inlines = [SurveyQuestionAndAnswerInline]
#### Survey




