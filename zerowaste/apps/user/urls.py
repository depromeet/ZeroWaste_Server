from django.urls import path, include

from apps.user.views import social_login, users, blocklist, auth, bazzi
# from rest_framework_jwt import views as jwt_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', users.UserViewSet)
router.register(r'blocklist', blocklist.BlockListViewSet)

admin_router = DefaultRouter()
admin_router.register(r'bazzi', bazzi.BazziViewSet)

urlpatterns = [
    # path('jwt-auth/', jwt_views.obtain_jwt_token),  # JWT 토큰 획득
    path('jwt-auth/refresh/', auth.CustomRefreshJSONWebToken.as_view()),
    path('jwt-auth/kakao/', social_login.KakaoLoginAPIView.as_view()),
    # path('api-jwt-auth/apple', views.AppleLoginAPIView.as_view()),
    path('users/double_check', users.double_check),
    path('', include(router.urls)),
    path('admin/', include(admin_router.urls))
]
