from django.contrib import admin
# from Istok_app.models import (Order, Furniture, Tags,
#                               FurnitureTags, FurniturePurpose, Purpose, ProjectImage, FurnitureImage, News, OrderImage)

from Istok_app import models

# istok_app_models = [models.Tags, models.FurnitureTags, models.FurniturePurpose, models.Purpose,
#                     models.ProjectImage, models.FurnitureImage, models.News, models.OrderImage]
istok_app_models = [models.Tags, models.Purpose, models.News, models.ProjectImage]

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

class PurposeInstanceInline(admin.TabularInline):
    model = models.FurniturePurpose

class TagsInstanceInline(admin.TabularInline):
    model = models.FurnitureTags

class ImageInstanceInline(admin.TabularInline):
    model = models.FurnitureImage


@admin.register(models.Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    model = models.Furniture
    list_display = ['name', 'id', 'type', "get_tags"]
    inlines = [PurposeInstanceInline, TagsInstanceInline, ImageInstanceInline]


class OrderImagesInline(admin.TabularInline):
    model = models.OrderImage


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    list_display = ['number', 'user', 'id', 'create_date', 'shipment_date', 'status', 'address']
    inlines = [OrderImagesInline]

