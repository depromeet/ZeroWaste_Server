from django.urls import path
from apps.user.views import social_login
from rest_framework_jwt import views as jwt_views

urlpatterns = [
    path('api/jwt-auth/', jwt_views.obtain_jwt_token),  # JWT 토큰 획득
    path('api/jwt-auth/refresh/', jwt_views.refresh_jwt_token),
    path('api/jwt-auth/kakao/', social_login.KakaoLoginAPIView.as_view()),
    # path('api-jwt-auth/apple', views.AppleLoginAPIView.as_view()),
    # path('test', views.test, name='test'),
]
