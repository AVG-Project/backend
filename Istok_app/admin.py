from django.contrib import admin
from Istok_app import models



<<<<<<< Updated upstream
istok_app_models = [models.Tags, models.News, models.ProjectImage, models.Application, models.FurnitureCategory,
                    models.Option, models.Answer]
=======
istok_app_models = [models.Tags, models.News, models.ProjectImage, models.FurnitureCategory,
                    models.Option, models.Answer, models.Order_Document]
>>>>>>> Stashed changes

admin.site.register(istok_app_models)


<<<<<<< Updated upstream
=======
#### Application
@admin.register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):
    model = models.Application
    list_display = ['date_time', 'phone', "status", 'id']
    list_filter = ('status',)
#### Application



#### Settings
>>>>>>> Stashed changes
@admin.register(models.WebsiteSettings)
class WebsiteSettingsAdmin(admin.ModelAdmin):
    model = models.WebsiteSettings
    list_display = ['name']


    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

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
    list_display = ['survey', 'question', 'id']
    inlines = [AnswerQuestionAndAnswerInline]
#### QuestionAndAnswer


#### Survey
# class QuestionAndAnswerInline(admin.TabularInline):
#     model = models.QuestionAndAnswer

@admin.register(models.Survey)
class SurveyAdmin(admin.ModelAdmin):
    model = models.Survey
    list_display = ['user', 'time_created', 'show_info']

    # def save_model(self, request, obj, form, change):
    #     """
    #     Given a model instance save it to the database.
    #     """
    #     update_fields = set()
    #     if change:
    #         for key, value in form.cleaned_data.items():
    #             # assuming that you have ManyToMany fields that are called groups and user_permissions
    #             # we want to avoid adding them to update_fields
    #             if key in ['user_permissions', 'groups']:
    #                 continue
    #             if value != form.initial[key]:
    #                 update_fields.add(key)
    #
    #     obj.save(update_fields=update_fields)
        
        
#### Survey




