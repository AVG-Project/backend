from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import generics, viewsets
from Istok_app.models import Furniture, Tags, News, Order, Application, FurnitureCategory, Question, \
    Survey, WebsiteSettings
from users.models import Loyalty, Benefit, LoyaltyBenefit
from . import serializers as my_serializers

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from .permissions import IsAdminOrReadOnly, SameUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, metadata, mixins

from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FurnitureFilter
from rest_framework.filters import OrderingFilter  # если импортировать по другому будет ошибка
from rest_framework import serializers
from django.http import Http404, HttpResponseForbidden
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()

# from rest_framework.generics import get_object_or_404


def variables(request):
    tags = list(Tags.objects.all().values())
    furniture_categories = list(FurnitureCategory.objects.all().values())

    return JsonResponse({'all_tags': tags, 'all_categories': furniture_categories})


#### User
class UserDetail(
                    # mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    # mixins.CreateModelMixin,
                    # mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = my_serializers.UserDetailSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        obj = get_object_or_404(User, pk=self.request.user.pk)
        return obj

# class UserCreate(
#                     # mixins.ListModelMixin,
#                     # mixins.RetrieveModelMixin,
#                     mixins.CreateModelMixin,
#                     # mixins.UpdateModelMixin,
#                     viewsets.GenericViewSet):
#
#     serializer_class = my_serializers.UserCreateSerializer
#
#
# class UserUpdate(
#                     # mixins.ListModelMixin,
#                     # mixins.RetrieveModelMixin,
#                     # mixins.CreateModelMixin,
#                     mixins.UpdateModelMixin,
#                     viewsets.GenericViewSet):
#
#     serializer_class = my_serializers.UserCreateSerializer
#     permission_classes = (IsAuthenticated, SameUser)
#
#     def get_object(self):
#         obj = get_object_or_404(User, pk=self.request.user.pk)
#         return obj

#########
# from djoser import views as djoser_views
# from rest_framework.decorators import action
#
# class CustomUserViewSet(djoser_views.UserViewSet):
#
#     @action(["post"], detail=False, url_path=f"set_email2")
#     def set_username(self, request, *args, **kwargs):
#         ret = super(CustomUserViewSet, self).set_username(request, *args, **kwargs)
#         print('\nСработал CustomUserViewSet set_username()\n')
#         return ret
#
#     @action(["post"], detail=False, url_path=f"reset_email")
#     def reset_username(self, request, *args, **kwargs):
#         ret = super(CustomUserViewSet, self).reset_username(request, *args, **kwargs)
#         print('\nСработал CustomUserViewSet reset_username()\n')
#         return ret



##########






def user_info(request):
    user = request.user
    user_loyalty = False
    user_survey = False
    is_authenticated = False
    if user.is_authenticated:
        is_authenticated = True
        try:
            if user.loyalty:
                user_loyalty = True
            if user.survey:
                user_survey = True
        except Exception as e:
            pass



    return JsonResponse({'is_authenticated': is_authenticated,
                         'user_loyalty': user_loyalty, 'user_survey': user_survey})
#### User


class FurniturePagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 1000



class FurnitureList(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = my_serializers.FurnitureListSerializer
    pagination_class = FurniturePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FurnitureFilter
    ordering_fields = ['price', 'time_created']
    permission_classes = (IsAdminOrReadOnly, )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.check_recommendations()
        serializer = my_serializers.ExtraFurnitureListSerializer(instance)
        return Response(serializer.data)

    def get_object(self):
        """Костыль для перепроверки наличия рекомендаций"""
        obj = super(FurnitureList, self).get_object()
        obj.check_recommendations()  # Костыль для перепроверки наличия рекомендаций
        return obj


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



class NewsList(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    # mixins.CreateModelMixin,
                    # mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = my_serializers.NewsListSerializer
    filter_backends = [OrderingFilter]
    ordering = ['-time_created']


    def get_queryset(self):
        print('\n\n')
        self.request.session.save()
        print(self.request.session.session_key)
        print(self.request.session)
        print(self.request.user.pk)
        print(self.request.user.is_authenticated)
        pk = self.kwargs.get('pk', None)
        if not pk:
            return News.objects.all().order_by('-time_created')
        return News.objects.filter(pk=pk)


class OrdersList(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = my_serializers.OrdersListSerializer
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

    serializer_class = my_serializers.ApplicationSerializer
    ordering = ['-time_created']


    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return Application.objects.all().order_by('-time_created')
        return Application.objects.filter(pk=pk)


#### Опросник и Анкета todo
class SurveyDetail(
                    # mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, )
    serializer_class = my_serializers.SurveySerializer
    ordering = ['-time_created']

    def get_object(self):
        obj = get_object_or_404(Survey, user_id=self.request.user.pk)
        return obj



class QuestionsList(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    # mixins.CreateModelMixin,
                    # mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):


    serializer_class = my_serializers.QuestionSerializer
    ordering = ['id']

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return Question.objects.all().order_by('id')
        return Question.objects.filter(pk=pk)

#### Опросник и Анкета


#### Loyalty Benefit

class LoyaltyDetail(
                    # mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    # mixins.CreateModelMixin,
                    # mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = my_serializers.LoyaltySerializer
    permission_classes = (IsAuthenticated,)


    def get_object(self):
        obj = get_object_or_404(Loyalty, user_id=self.request.user.pk)
        return obj



class LoyaltyBenefitUpdate(  # mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    # mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = my_serializers.LoyaltyBenefitSerializer


    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        return LoyaltyBenefit.objects.filter(pk=pk)



class WebsiteSettingsList(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = WebsiteSettings.objects.all()
    serializer_class = my_serializers.WebsiteSettingsSerializer


# class BenefitList(mixins.ListModelMixin,
#                 # mixins.RetrieveModelMixin,
#                 # mixins.CreateModelMixin,
#                 # mixins.UpdateModelMixin,
#                 viewsets.GenericViewSet):
#
#     serializer_class = BenefitSerializer
#
#     def get_queryset(self):
#         return Benefit.objects.all().order_by('id')

#### Loyalty Benefit





# from collections import Counter
#
#
# def test(request, pk):
#     obj = get_object_or_404(Furniture, pk=pk)
#     obj_tags = obj.tags.values_list('id')
#
#     similar_objs = Furniture.objects.filter(category_id=obj.category_id, tags__in=obj.tags.all()).\
#         exclude(pk=pk)
#     similar_objs_dct = Counter(similar_objs.values_list('id', flat=True))
#     sorted_similar = sorted(similar_objs_dct.items(), key=lambda item: item[1], reverse=True)[:3]
#     lst_sorted = [_[0] for _ in sorted_similar]
#     ready_similar = Furniture.objects.filter(pk__in=lst_sorted)
#
#
#
#     return JsonResponse({'obj': obj.name, 'obj_tags': list(obj_tags),
#                          'similar_objs': list(similar_objs.values_list('id', flat=True)),
#                          # 'new_obj_tags': list(similar_objs.values('name')),
#                          'similar_objs_dct': similar_objs_dct,
#                          'lst_sorted': lst_sorted,
#                          'ready_similar': list(ready_similar.values()),
#
#                          })




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

