from django.contrib import admin

from Istok_app import models



istok_app_models = [models.Tags, models.News, models.ProjectImage, models.Application, models.FurnitureCategory]

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

class TagsInstanceInline(admin.TabularInline):
    model = models.FurnitureTags

class ImageInstanceInline(admin.TabularInline):
    model = models.FurnitureImage


@admin.register(models.Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    model = models.Furniture
    list_display = ['category', 'name', 'id', "get_tags"]
    inlines = [TagsInstanceInline, ImageInstanceInline]


class OrderImagesInline(admin.TabularInline):
    model = models.OrderImage


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    list_display = ['number', 'user', 'id', 'create_date', 'shipment_date', 'status', 'address']
    inlines = [OrderImagesInline]

