from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import generics, viewsets
from Istok_app.models import Furniture, Tags, Purpose, News, Order, Application
from .serializers import FurnitureListSerializer, NewsListSerializer, OrdersListSerializer, ApplicationSerializer

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, metadata, mixins
from .permissions import IsAdminOrReadOnly
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FurnitureFilter
from rest_framework.filters import OrderingFilter  # если импортировать по другому будет ошибка


class FurniturePagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000



class FurnitureList(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    # mixins.CreateModelMixin,
                    # mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = FurnitureListSerializer
    pagination_class = FurniturePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FurnitureFilter
    ordering_fields = ['price', 'time_created']
    # permission_classes = (IsAdminOrReadOnly, )


    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return Furniture.objects.all().order_by('-id')
        return Furniture.objects.filter(pk=pk)


def choice_list_to_dict(lst_of_tup):
    lst = []
    for tup in lst_of_tup:
        lst.append({'id': tup[0], 'name': tup[1]})
    return lst


def variables(request):
    furniture_types = choice_list_to_dict(Furniture.TYPES)
    furniture_forms = choice_list_to_dict(Furniture.FORMS)
    tabletop_materials = choice_list_to_dict(Furniture.TABLETOP_MATERIAL)
    furniture_materials = choice_list_to_dict(Furniture.MATERIAL)
    furniture_styles = choice_list_to_dict(Furniture.STYLES)
    purposes = list(Purpose.objects.all().values())
    # order_statuses = choice_list_to_dict(Order.STATUSES)
    filter_items = [
        {'name': 'Типы мебели', 'options': furniture_types},
        {'name': 'Формы', 'options': furniture_forms},
        {'name': 'Материалы столешниц', 'options': tabletop_materials},
        {'name': 'Материалы фасадов', 'options': furniture_materials},
        {'name': 'Стили', 'options': furniture_styles},
        {'name': 'Назначения', 'options': purposes},
        # {'name': 'Статусы доставок', 'options': order_statuses},
    ]

    return JsonResponse({'filter_items': filter_items})


class NewsList(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    # mixins.CreateModelMixin,
                    # mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = NewsListSerializer
    filter_backends = [OrderingFilter]
    ordering = ['-time_created']


    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return News.objects.all().order_by('-time_created')
        return News.objects.filter(pk=pk)


class OrdersList(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = OrdersListSerializer
    ordering = ['-create_date']


    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return Order.objects.all().order_by('-create_date')
        return Order.objects.filter(pk=pk)


class ApplicationsList(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = ApplicationSerializer
    ordering = ['-time_created']


    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return Application.objects.all().order_by('-time_created')
        return Application.objects.filter(pk=pk)




# class FurnitureSet(viewsets.ModelViewSet):
#     serializer_class = FurnitureListSerializer
#     pagination_class = FurniturePagination
#
#
#
#     def get_queryset(self):
#         pk = self.kwargs.get('pk', None)
#         if not pk:
#             return Furniture.objects.all().order_by('-id')
#         return Furniture.objects.filter(pk=pk)
#
#
#     # @action(methods=['get'], detail=True)
#     # def tags(self, request, pk=None):
#     #     tags = Tags.objects.get(pk=pk)
#     #     return Response({'tags': tags.name})
#
#
#
#     def destroy(self, request, *args, **kwargs):
#         if request.user.is_staff:
#             instance = self.get_object()
#             id = instance.pk
#             name = instance.name
#             self.perform_destroy(instance)
#             return Response({"furniture": f"furniture id={id} name={name} deleted"})
#         else:
#             return Response(status=status.HTTP_403_FORBIDDEN)





# class ProjectImageApiDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = P.objects.all()
#     serializer_class = FinishedFurnitureSerializer



# Через Apiview
# class FinishedFurnitureApiView(APIView):
#     def get(self, request):
#         f = Finished_furniture.objects.all()
#         return Response({'finished_furniture': FinishedFurnitureSerializer(f, many=True).data})
#
#     def post(self, request):
#         serializer = FinishedFurnitureSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'finished_furniture': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         id = kwargs.get('id', None)
#         if not id:
#             return Response({'error': "Метод PUT требует ID объекта который будет изменен"})
#         try:
#             instance = Finished_furniture.objects.get(pk=id)
#         except:
#             return Response({'error': f'Объект Finished_furniture с ID={id} не существует'})
#         serializer = FinishedFurnitureSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"finished_furniture": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         id = kwargs.get("id", None)
#         if not id:
#             return Response({'error': 'Метод DELETE не разрешен'})
#         elif Finished_furniture.objects.filter(pk__exact=id).exists():
#             Finished_furniture.objects.get(pk=id).delete()
#             return Response({'finished_furniture': f'Удален объект Finished_furniture(id={id})'})
#         else:
#             #ID в запросе присутствует, но такого объекта нет
#             return Response({'finished_furniture': f'Объект с Finished_furniture(id={id}) не существует'})
#
# finished_furniture_api = FinishedFurnitureApiView.as_view()


# Через модели API
# class FinishedFurnitureApiList(generics.ListAPIView):
#     queryset = Finished_furniture.objects.all()
#     serializer_class = FinishedFurnitureSerializer
#
#
# finished_furniture_list = FinishedFurnitureApiList.as_view()
#
#
# class FinishedFurnitureApiDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Finished_furniture.objects.all()
#     serializer_class = FinishedFurnitureSerializer
#
#
# finished_furniture_detail = FinishedFurnitureApiDetail.as_view()

