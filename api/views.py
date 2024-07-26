from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import generics, viewsets
from Istok_app.models import Furniture, Tags
from .serializers import ListFurnitureSerializer
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


class FurniturePagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000






class FurnitureList(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    # mixins.CreateModelMixin,
                    # mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = ListFurnitureSerializer
    pagination_class = FurniturePagination
    # permission_classes = (IsAdminOrReadOnly, )



    def list_view_change(self, data):
        pass


    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return Furniture.objects.all().order_by('-id')
        return Furniture.objects.filter(pk=pk)



def variables(request):
    all_furniture_type = dict(Furniture.TYPES)
    all_furniture_forms = dict(Furniture.FORMS)
    all_furniture_material = dict(Furniture.MATERIAL)
    all_furniture_styles = dict(Furniture.STYLES)
    return JsonResponse({'all_furniture_type': all_furniture_type, 'all_furniture_forms': all_furniture_forms,
                     'all_furniture_material': all_furniture_material, 'all_furniture_styles': all_furniture_styles, })








# class FurnitureSet(viewsets.ModelViewSet):
#     serializer_class = ListFurnitureSerializer
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

