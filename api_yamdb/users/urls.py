from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignupView, UserViewSet, TokenObtainView

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

auth_urls = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('token/', TokenObtainView.as_view(), name='token_obtain'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_v1.urls)),
]
