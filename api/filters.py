from django_filters import FilterSet
from Istok_app.models import Furniture
from django_filters import rest_framework as filters



class CharFilterInFilter(filters.CharFilter, filters.BaseInFilter):
    pass


class FurnitureFilter(filters.FilterSet):
    tags_name = filters.CharFilter(field_name='tags__name', lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')


    class Meta:
        model = Furniture
        fields = ['min_price', 'max_price', 'tags_name', 'category', 'tags']


