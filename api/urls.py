from django.urls import path, include, re_path
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'furniture_list', views.FurnitureList, basename='furniture_list')
router.register(r'news_list', views.NewsList, basename='news_list')
router.register(r'orders_list', views.OrdersList, basename='orders_list')
router.register(r'applications_list', views.ApplicationsList, basename='applications_list')
router.register(r'questions_list', views.QuestionsList, basename='questions_list')
# router.register(r'survey_detail', views.SurveyDetail, basename='survey_detail')
router.register(r'loyalty_detail', views.LoyaltyDetail, basename='loyalty_detail')
router.register(r'loyalty_benefit', views.LoyaltyBenefitUpdate, basename='loyalty_benefit')
router.register(r'website_settings_list', views.WebsiteSettingsList, basename='website_settings_list')



urlpatterns = [
    path("api/v1/", include(router.urls)),  # http://127.0.0.1:8000/api/v1/finished_furniture/

    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/variables/', views.variables),
    path('api/v1/user_info/', views.user_info),
    # path('api/v1/test/<int:pk>/', views.test),
    path('api/v1/survey_detail/', views.SurveyDetail.as_view({'get': 'retrieve', 'post': 'create',
                                                              'put': 'update', 'patch': 'update'})),
]
