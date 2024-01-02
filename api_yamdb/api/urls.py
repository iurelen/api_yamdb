from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('reviews', ReviewViewSet)
router_v1.register('comments', CommentViewSet)
router_v1.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/titles/<int:post_id>/', include(router_v1.urls)),
]