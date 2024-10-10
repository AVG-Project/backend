from django.urls import path, include, re_path
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


router = routers.DefaultRouter()
router.register(r'furniture_list', views.FurnitureList, basename='furniture_list')
router.register(r'news_list', views.NewsList, basename='news_list')
router.register(r'orders_list', views.OrdersList, basename='orders_list')
router.register(r'applications_list', views.ApplicationsList, basename='applications_list')
router.register(r'questions_list', views.QuestionsList, basename='questions_list')
# router.register(r'survey_detail', views.SurveyDetail, basename='survey_detail')
# router.register(r'loyalty_detail', views.LoyaltyDetail, basename='loyalty_detail')
router.register(r'loyalty_benefit', views.LoyaltyBenefitUpdate, basename='loyalty_benefit')
router.register(r'website_settings_list', views.WebsiteSettingsList, basename='website_settings_list')
# router.register(r'loyalty_detail', views.LoyaltyDetail.as_view({'get': 'retrieve'}), basename='loyalty_detail')
########
# router.register("users", views.CustomUserViewSet)
########



urlpatterns = [
    path("api/v1/", include(router.urls)),  # http://127.0.0.1:8000/api/v1/finished_furniture/

    path('api/v1/drf-auth/', include('rest_framework.urls')),

    path('api/v1/auth/', include('djoser.urls')),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    path('api/v1/variables/', views.variables),
    path('api/v1/user_info/', views.user_info),
    # path('api/v1/test/<int:pk>/', views.test),
    path('api/v1/survey_detail/', views.SurveyDetail.as_view({'get': 'retrieve', 'post': 'create',
                                                              'put': 'update', 'patch': 'update'})),
    path('api/v1/loyalty_detail/', views.LoyaltyDetail.as_view({'get': 'retrieve'})),

    path('api/v1/user_detail/', views.UserDetail.as_view({'get': 'retrieve'})),
    # path('api/v1/user_create/', views.UserCreate.as_view({'post': 'create'})),
    # path('api/v1/user_update/', views.UserUpdate.as_view({'put': 'update', 'patch': 'update'})),
]

