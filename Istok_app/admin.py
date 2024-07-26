from django.contrib import admin
from Istok_app.models import (Orders, Furniture, Application, Parts, Tags,
                              FurnitureTags, FurniturePurpose, Purpose, ProjectImage, FurnitureImage)


istok_app_models = [Tags, Orders, Application, Parts, FurnitureTags,
                    FurniturePurpose, Purpose, ProjectImage, FurnitureImage]


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


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    model = Furniture
    list_display = ['name', 'id', 'type', "get_tags"]


