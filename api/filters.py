from django_filters import FilterSet
from Istok_app.models import Furniture
from django_filters import rest_framework as filters



class CharFilterInFilter(filters.CharFilter, filters.BaseInFilter):
    pass


class FurnitureFilter(filters.FilterSet):
    tags = CharFilterInFilter(field_name='tags__id', lookup_expr='in')
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    purposes = CharFilterInFilter(field_name='purposes__id', lookup_expr='in')


    class Meta:
        model = Furniture
        fields = ['min_price', 'max_price', 'tags', 'purposes', 'style', 'facades_material', 'form']

