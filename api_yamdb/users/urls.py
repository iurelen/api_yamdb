from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from .views import SignupView, CustomUserViewSet

app_name = 'users'

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
# router.register('users/me', GetUserViewSet, basename='users_me')

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),  # refresh объединить в /auth/token/
    path('', include(router.urls)),
    # path('users/me/', GetUserView.as_view(), name='user_info')
]
